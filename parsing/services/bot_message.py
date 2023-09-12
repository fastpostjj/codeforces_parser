import requests
from config.settings import BOT_URL, BOT_TOKEN
from config.settings import BASE_DIR
from django.utils import timezone
import os


class Bot_message():
    """
    класс Bot_message для отправки и получения сообщений телеграм-бота
    """

    def __init__(self) -> None:
        """
        инициализация объекта бота
        """
        self.token = BOT_TOKEN
        self.url_bot = BOT_URL

    def get_url(self, *args, **kwargs) -> str:
        """
        возвращает url для api бота
        """
        method = kwargs.get('method')
        self.url = f'{self.url_bot}{self.token}/{method}'
        return self.url

    def send_message(self, *args, **kwargs):
        """
        отправка сообщения пользователю телеграм
        """
        url = self.get_url(method='sendMessage')
        chat_id = kwargs.get('chat_id')
        text = kwargs.get('text')
        response = requests.get(url, params={'chat_id': chat_id, 'text': text})

        # Пишем в лог-файл
        file_name = str(BASE_DIR) + os.sep + "bot_log.txt"
        text = f"{timezone.now()} send_message kwargs=" +\
            "{kwargs} {chat_id} {text} {response.json()}\n"
        datetime_now = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
        with open(file_name, "a", encoding="utf-8") as file:
            file.write(f"{datetime_now} {text}\n")

        return response.status_code
