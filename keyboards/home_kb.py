from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

b1 = KeyboardButton('✍На главную')

kb_home = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
kb_home.row(b1)