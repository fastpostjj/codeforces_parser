from parsing.models import Subscriptions, Problems
from parsing.services.services import GetProblems
from parsing.services.bot_message import Bot_message
from config.settings import LOG_FILE
from django.utils import timezone


class MessageCreator():
    """
    Класс рассылки задач пользователям в соответствии
    с их подписками
    """
    def __init__(self):
        self.log_file_name = LOG_FILE

    def save_log(self, text: str) -> None:
        datetime_now = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file_name, "a", encoding="utf-8") as file:
            file.write(f"{datetime_now} {text}\n")

    def make_text_for_send(self, problems):
        text = ""
        if not isinstance(problems, Problems) and len(problems) > 1:
            for problem in problems:
                text += str(problem) + "\n" + problem.get_url() + "\n"
        else:
            text += str(problems) + "\n" + problems.get_url() + "\n"
        return text

    def get_subscriptions(self, *args, **kwargs):
        sub = Subscriptions.objects.filter(is_active=True)
        return sub


def send_messages():
    """
    выбираем все активные подписки и рассылаем задачи
    """
    number = 5 # количество отправляемых задач за один раз
    creator = MessageCreator()
    subs = creator.get_subscriptions()
    for sub in subs:
        problems = GetProblems().get_problems_by_tag(
            tag=sub.tag,
            contest=sub.contest,
            number=number
            )
        text = creator.make_text_for_send(problems)
        bot = Bot_message()
        return bot.send_message(
            chat_id=sub.user.chat_id,
            text=text
            )
    creator.save_log("send messages")