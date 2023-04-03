from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client, kb_scenario, kb_pattern, kb_home
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from config import db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class FSMClient(StatesGroup):
    name = State()
    text = State()
    new_name = State()
    new_text = State()


async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Добро пожаловать, нажмите на кнопку <b>"Запустить сценарий"</b>👇 чтобы приступить к редактированию СМС и отправке', reply_markup=kb_client, parse_mode='HTML')
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему👇\n\n@my_aiogram_assist_bot')


async def select_scenario(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Текст будем отправлять из шаблона или пишем руками👇', reply_markup=kb_scenario, parse_mode='HTML')
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему👇\n\n@my_aiogram_assist_bot')


async def pattern_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Добавим новый шаблон или внесем правки в существующий?👇', reply_markup=kb_pattern, parse_mode='HTML')
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему👇\n\n@my_aiogram_assist_bot')


async def pattern_start_new(message: types.Message):
    await bot.send_message(message.from_user.id, f'Укажите имя шаблона👇')
    await FSMClient.name.set()


async def send_pattern_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await bot.send_message(message.from_user.id, f'Напишите текст шаблона👇')
    await FSMClient.text.set()


async def send_pattern_text(message: types.Message, state: FSMContext):
    text = message.text
    await state.update_data(text=text)
    data = await state.get_data()
    db.add_pattern(name=data['name'], text=data['text'])
    await bot.send_message(message.from_user.id, f'Шаблон успешно сохранен', reply_markup=kb_home)
    await state.finish()


async def start_change_pattern(message: types.Message):
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
    await FSMClient.new_name.set()


async def send_shablon(callback_query: types.CallbackQuery, state: FSMContext):
    name = callback_query.data
    await state.update_data(name=name)
    await callback_query.message.answer('Введите новый текст шаблона👇')
    await FSMClient.new_text.set()


async def send_new_text(message: types.Message, state: FSMContext):
    text = message.text
    await state.update_data(text=text)
    data = await state.get_data()
    db.update_text(text=data['text'], name=data['name'])
    await bot.send_message(message.from_user.id, f'Текст успешно заменил', reply_markup=kb_home)
    await state.finish()


async def restart_fsm(message: types.Message, state: FSMContext = None):
    await bot.send_message(message.from_user.id, 'машина состояний сброшена - делай что хочешь😏', reply_markup=kb_home)
    if state:
        await state.finish()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(command_start, Text(equals='✍На главную', ignore_case=True))
    dp.register_message_handler(restart_fsm, commands=['restart_fsm'], state='*')
    dp.register_message_handler(select_scenario, Text(equals='📩Запустить сценарий', ignore_case=True), state=None)
    dp.register_message_handler(pattern_start, Text(equals='🛠Работа с шаблонами смс', ignore_case=True))
    dp.register_message_handler(pattern_start_new, Text(equals='🆕Новый шаблон', ignore_case=True), state=None)
    dp.register_message_handler(send_pattern_name, state=FSMClient.name)
    dp.register_message_handler(send_pattern_text, state=FSMClient.text)
    dp.register_message_handler(start_change_pattern, Text(equals='🔨Вносим правки', ignore_case=True), state=None)

    dp.register_callback_query_handler(send_shablon, state=FSMClient.new_name)
    dp.register_message_handler(send_new_text, state=FSMClient.new_text)