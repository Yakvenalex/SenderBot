from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

b1 = KeyboardButton('✍️Написать')
b2 = KeyboardButton('🔍Выбрать из шаблона')

kb_scenario = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
kb_scenario.row(b1, b2)