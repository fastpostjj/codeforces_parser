from config.celery import app
from parsing.services.codeforces_parser import CodeforcesParser
from parsing.services.message_creator import send_messages


@app.task
def check_update(*args):
    """
    периодическая задача проверки обновления задач
    """
    conn = CodeforcesParser()
    conn.get_update()


@app.task
def send_messages_every_day(*args):
    """
    периодическая задача рассылки задач по подписке
    """
    send_messages()
