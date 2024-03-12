from aiogram.fsm.state import StatesGroup, State

class Item(StatesGroup):
    info = State()
    get_db = State()