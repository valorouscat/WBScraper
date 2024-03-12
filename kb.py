from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
menu = [
    [InlineKeyboardButton(text="Получить информацию по товару", callback_data="get_info")],
    [InlineKeyboardButton(text="Остановить уведомления", callback_data="unsubscribe")],
    [InlineKeyboardButton(text="Получить информацию из БД", callback_data="get_db_data")],
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Меню")]], resize_keyboard=True)
subscribe_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Подписаться", callback_data="subscribe")]])