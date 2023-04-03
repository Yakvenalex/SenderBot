from aiogram import types, Dispatcher
from create_bot import dp

# @dp.message_handler()
async def echo_send(message: types.Message):
    if 'привет' in message.text.lower():
        await message.reply('Ну привет. Чё те надо тут?')



def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo_send)