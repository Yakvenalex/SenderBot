from dotenv import load_dotenv
import os
from sms77api.Sms77api import Sms77api

# Загрузить переменные среды из файла .env
load_dotenv()


def send_message(Sender_Name, Phone, Text):
    client = Sms77api(os.getenv('SMS_API'))
    params = {'json': True, 'from': Sender_Name}
    print(client.sms(Phone, Text, params))


send_message('Alfa_Dog', "335121,1424124,41241412", 'Тестовый текст')

