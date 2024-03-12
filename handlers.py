from aiogram import types, F, Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import flags
from aiogram.fsm.context import FSMContext
import utils
import logging
from states import Item
import asyncio
import re
import json
import kb
from db import get_session, Item_line

logger = logging.getLogger(__name__)

with open("text.json", "r", encoding="utf-8") as f:
    text = json.load(f)

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    logger.info(f"User {msg.from_user.id} started bot")
    await msg.answer(text['greet'], reply_markup=kb.menu)


@router.message(F.text == "Меню")
@router.message(F.text == "меню")
async def menu(msg: Message):
    logger.info(f"User {msg.from_user.id} requested menu")
    await msg.answer(text['menu'], reply_markup=kb.menu)


@router.callback_query(F.data == "get_info")
async def input_item_id(clbck: types.CallbackQuery, state: FSMContext):
    logger.info(f"User {clbck.from_user.id} requested get_info") 
    await state.set_state(Item.info)
    await clbck.message.edit_text(text['item_text'])
    await clbck.message.answer(text['exit'], reply_markup=kb.exit_kb)


@router.callback_query(F.data == "get_db_data")
async def get_db_data(clbck: types.CallbackQuery, state: FSMContext):
    logger.info(f"User {clbck.from_user.id} requested get_db_data")
    with get_session() as session:
        db_data = session.query(Item_line).order_by(Item_line.id.desc()).limit(5).all()
        if not db_data:
            return await clbck.message.edit_text(text['no_data'])
        result = []
        for item in db_data:
            result.append(str(item))
        await clbck.message.edit_text(text='\n'.join(result), reply_markup=kb.menu)


@router.message(Item.info)
@flags.chat_action("typing")
async def get_info(message: Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} requested item info for id {message.text}")
    id = message.text
    msg = await message.answer(text['wait'])
    result = utils.get_info(id, message.from_user.id)
    if not result: 
        logger.warning(f"User {message.from_user.id} failed to get item info for id {id}")
        return await msg.edit_text(text['error'])
    await msg.edit_text(result, reply_markup=kb.subscribe_kb)


async def send_message_task(callback, message):
    while True:
        logger.info(f"Sending message to {callback.from_user.id}")
        await asyncio.sleep(300)
        await callback.message.answer(text=message)


@router.callback_query(F.data == "subscribe")
async def subscribe_for_item(clbck: types.CallbackQuery):
    logger.info(f"User {clbck.from_user.id} subscribed for item")
    pattern = r"Артикул:\s*(\d+)"
    match = re.search(pattern, clbck.message.text)
    id = match.group(1)
    global mailing_task
    mailing_task = asyncio.create_task(send_message_task(clbck, utils.get_info(id, clbck.from_user.id)))
    await mailing_task
    await clbck.message.answer(text['subscribed'], reply_markup=kb.menu)


@router.callback_query(F.data == "unsubscribe")
async def unsubscribe(clbck: types.CallbackQuery):
    try:
        logger.info(f"User {clbck.from_user.id} unsubscribed")
        if mailing_task:
            mailing_task.cancel()
            await clbck.message.edit_text(text['unsubscribed'], reply_markup=kb.menu)
        else:
            await clbck.message.edit_text(text['not_subscribed'], reply_markup=kb.menu)
    except NameError:
        await clbck.message.edit_text(text['not_subscribed'], reply_markup=kb.menu)
