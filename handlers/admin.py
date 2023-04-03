from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from create_bot import dp, bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import db
from keyboards import kb_home
from dotenv import load_dotenv
import os
from sms77api.Sms77api import Sms77api
import asyncio

load_dotenv()
client = Sms77api(os.getenv('SMS_API'))


def count_phone(phone):
    phone_list = phone.split(',')
    return phone_list


class FSMAdmin(StatesGroup):
    name_find = State()
    text = State()
    text_my = State()
    phone = State()
    name_company = State()
    link = State()


async def start_send_message_2(message: types.Message):
    list_data = []
    for i in db.select_all_pattern():
        list_data.append({i[0]: i[1]})
    inkb = InlineKeyboardMarkup()
    row = []
    for x in list_data:
        pattern_key = list(x.keys())[0]
        btn = InlineKeyboardButton(text=pattern_key, callback_data=pattern_key)
        row.append(btn)
        if len(row) == 2:
            inkb.row(*row)
            row = []
    if row:
        inkb.row(*row)
    await message.answer('Выберите шаблон сообщения👇', reply_markup=inkb)
    await FSMAdmin.text.set()


async def send_shablon(callback_query: types.CallbackQuery, state: FSMContext):
    text = db.select_pattern(name=callback_query.data)[1]
    await state.update_data(text=text)
    await callback_query.answer(f'Вы выбрали шаблон {callback_query.data}')
    await callback_query.message.answer('Кому отправляем смс? (укажите номера через запятую)👇')
    await FSMAdmin.phone.set()


async def inline_phone(message: types.Message, state: FSMContext):
    phone = message.text
    await state.update_data(phone=phone)
    await bot.send_message(message.from_user.id, f'Имя компании👇')
    await FSMAdmin.next()


async def send_name_company_2(message: types.Message, state: FSMContext):
    name_company = message.text
    await state.update_data(name_company=name_company)
    await bot.send_message(message.from_user.id, f'Вставьте ссылку👇')
    await FSMAdmin.link.set()


async def send_link_2(message: types.Message, state: FSMContext):
    link = message.text
    await state.update_data(link=link)
    data = await state.get_data()
    sms_text = data["text"]
    sender_name = str(data["name_company"])
    phone_list = count_phone(data['phone'])

    for phone in phone_list:
        # await bot.send_message(message.from_user.id, f'Сообщение от: <b>{sender_name}</b>\n'
        #                                              f'Сообщение отправляю на номер: <b>{phone}</b>\n\n'
        #                                              f'{sms_text}\n'
        #                                              f'<b>Ссылка</b>: {link}\n\n', parse_mode='HTML')
        try:
            client.sms(phone, f'{sms_text}:\n{link}', {'json': True, 'from': sender_name})
        except Exception as EX:
            print(EX)

    await bot.send_message(message.from_user.id, 'Все сообщения успешно отправлены', reply_markup=kb_home)

    await state.finish()
    await bot.send_message(message.from_user.id, f'Инфоормацию успешно отправил')


async def start_send_message(message: types.Message):
    await bot.send_message(message.from_user.id, f'Напишите текст отправляемого смс👇')
    await FSMAdmin.text_my.set()


async def send_text(message: types.Message, state: FSMContext):
    text = message.text
    await state.update_data(text=text)
    await bot.send_message(message.from_user.id, f'Кому отправляем смс? (укажите номера через запятую)👇')
    await FSMAdmin.phone.set()


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(start_send_message, Text(equals='✍️Написать', ignore_case=True), state=None)
    dp.register_message_handler(start_send_message_2, Text(equals='🔍Выбрать из шаблона', ignore_case=True), state=None)
    dp.register_callback_query_handler(send_shablon, state=FSMAdmin.text)
    dp.register_message_handler(inline_phone, state=FSMAdmin.phone)
    dp.register_message_handler(send_name_company_2, state=FSMAdmin.name_company)
    dp.register_message_handler(send_link_2, state=FSMAdmin.link)
    dp.register_message_handler(send_text, state=FSMAdmin.text_my)
