import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import Config
from handlers import router


logging.getLogger().name = __name__
logging.basicConfig(filename='logs.log', filemode='w', level=logging.INFO, format='%(asctime)s - %(name)-14s - %(levelname)-8s - %(message)s')


async def main():
    bot = Bot(token=Config.TG_BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())