from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('🆕Новый шаблон')
b2 = KeyboardButton('🔨Вносим правки')

kb_pattern = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
kb_pattern.row(b1, b2)