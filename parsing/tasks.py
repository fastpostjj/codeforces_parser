from config.celery import app
from parsing.services.codeforces_parser import CodeforcesParser


@app.task
def check_update(*args):
    """
    периодическая задача проверки обновления задач
    """
    conn = CodeforcesParser()
    conn.get_update()
