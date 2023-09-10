import requests
from user_auth.models import User
# from habits.models import Habits
from parsing.models import BotMessages
from config.settings import BOT_URL, bot_token
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
        self.token = bot_token
        self.url_bot = BOT_URL

    def get_url(self, *args, **kwargs) -> str:
        """
        возвращает url для api бота
        """
        method = kwargs.get('method')
        self.url = f'{self.url_bot}{self.token}/{method}'
        return self.url

    # def get_last_message_id(self) -> int:
    #     """
    #     Находит самое последнее сохраненное сообщение в базе для дальнейшей
    #     проверки новых сообщений
    #     """
    #     last_message_id = BotMessages.objects.all().order_by("-id").first()
    #     if last_message_id:
    #         return last_message_id.message_id
    #     return 0

    def send_list_or_gen_password(self, chat_id, first_name):
        """
        в ответ на новое сообщение отправляет:
         - новому пользователю генерирует пароль и добавляет в базу данных
         - существующему пользователю список его привычек
        """
        if User.objects.filter(chat_id=chat_id).exists():
            # Пользователь уже есть в базе.
            # Отправляем ему список его привычек
            user = User.objects.get(chat_id=chat_id)
            message = "Список ваших привычек:\n"
            habits = Habits.objects.filter(user=user)
            for habit in habits:
                message += str(habit) + "\n"
            self.send_message(
                chat_id=chat_id,
                text=message
            )
        else:
            # Новому пользователю генерируем пароль
            # для доступа и заносим его в базу
            password = self.generate_new_password()
            user = User.objects.create(
                chat_id=chat_id,
                first_name=first_name,
                email='test@test.ru',
                is_staff=False,
                is_superuser=False
            )
            user.set_password(password)
            user.save()
            self.send_message(
                chat_id=chat_id,
                text=f"Ваш id {chat_id} добавлен в базу.\n"
                + f" Вам установлен пароль для доступа к сайту:\n{password}.\n"
                + " Вы можете настроить список привычек для рассылки " +
                "напоминаний.\n"
                + " Для начала отправки необходимо установить пользователю " +
                "статус is_subscripted=True.\n"
            )
        return user

    def get_updates(self, *args, **kwargs):
        """
        проверка новых сообщений в чате
        """
        last_message_id = self.get_last_message_id()
        url = self.get_url(method='getUpdates')
        response = requests.get(
            url,
        ).json()
        if response['ok'] is True:
            result = response['result']
            for update in result:
                message = update['message']
                message_id = message['message_id']
                text = message['text']
                chat_id = message['chat']['id']
                first_name = message['chat']['first_name']
                if message_id > last_message_id:
                    # Нового пользователя добавляем в базу, существующему
                    # отправляем список его привычек
                    user = self.send_list_or_gen_password(chat_id, first_name)
                    # Новое сообщение сохраняем в базу
                    new_message = BotMessages.objects.create(
                        message_id=message_id,
                        message_text=text,
                        user=user
                    )
                    new_message.save()
        else:
            file_name = str(BASE_DIR) + os.sep + "log.txt"
            text = f"{timezone.now()} check new messages: " +\
                f"Ответ не подлежит обработке: {response}"
            with open(file_name, "a", encoding="utf-8") as file:
                file.write(text)
            return False

    def send_message(self, *args, **kwargs):
        """
        отправка сообщения пользователю телеграм
        """
        url = self.get_url(method='sendMessage')
        chat_id = kwargs.get('chat_id')
        text = kwargs.get('text')
        response = requests.get(url, params={'chat_id': chat_id, 'text': text})

        file_name = str(BASE_DIR) + os.sep + "log.txt"

        text = f"{timezone.now()} send_message kwargs=" +\
            "{kwargs} {chat_id} {text} {response.json()}\n"
        with open(file_name, "a", encoding="utf-8") as file:
            file.write(text)

        return response.status_code
