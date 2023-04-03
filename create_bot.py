import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

# Загрузить переменные среды из файла .env
load_dotenv()

storage = MemoryStorage()
bot = Bot(token=os.getenv('API_KEY'))
dp = Dispatcher(bot, storage=storage)