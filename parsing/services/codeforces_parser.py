import requests
import json
from config.settings import URL, URL_PROBLEM, LOG_FILE
from django.utils import timezone
from parsing.models import Problems, Tags


"""
Ответом на каждый запрос является JSON-объект с тремя возможными полями: status,
comment и result.

Статус может быть "OK" или "FAILED".
Если status равен "FAILED", то поле comment содержит причину, по которой запрос
не получилось выполнить. Если status равен "OK", то поле comment отсутствует.
Если status равен "OK", то поле result содержит результат запроса в формате JSON,
который зависит от метода и для каждого метода описан отдельно. Если status равен
"FAILED", то поле result отсутствует.

Поля, зависящие от языка, будут возвращаться с использованием языка по умолчанию.
Вы можете передать дополнительный параметр lang с значениями en и ru для того,
чтобы явно указать язык результата.
"""


class CodeforcesParser():
    """
    Класс CodeforcesParser для работы с API сайта https://codeforces.com/,
    на котором размещены задачи
    """
    def __init__(self):
        self._url = URL

    # @property
    def save_log(self, text):
        datetime_now = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a", encoding="utf-8") as file:
            file.write(f"{datetime_now} {text}\n")

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    def get_data_from_site(self) -> str:
        """
        метод посылает запрос на сайт и возвращает полученные данные
        """
        method = "problemset.problems"
        try:
            response = requests.get(
                f"{self.url}{method}",
                {
                    "lang": "ru"
                })
        except Exception as error:
            print("Ошибка получения данных", error)
            self.save_log(f"Ошибка получения данных {error}")

        if response.status_code == 200:
            if response.json()["status"] == "OK":
                result = response.json()
                problems = result["result"]["problems"]

                # сохраняем полученные данные в файл
                with open("res.json", mode="w", encoding="utf-8") as file:
                    json.dump(result, file)
                return result
            else:
                # comment содержит текст ошибки
                print(response.json()["comment"])
                self.save_log(response.json()["comment"])
        else:
            print("Ошибка при выполнении запроса")
            self.save_log("Ошибка при выполнении запроса")

    def get_from_file(self):
        with open("res.json", mode="r", encoding="utf-8") as file:
            result = json.load(file)
            return result

    def get_update(self):
        """
        разбираем полученные данные
        """
        result = self.get_data_from_site()
        # result = self.get_from_file()

        if result["status"] == "OK":
            problems = result["result"]["problems"]
            problemStatistics = result["result"]["problemStatistics"]
            counter_problems = Problems.objects.all().count()
            counter_tags = Tags.objects.all().count()

            with open("res.json", mode="w", encoding="utf-8") as file:
                json.dump(result, file)
            for problem in problems:
                if 'name' in problem and \
                        'index' in problem and \
                        'contestId' in problem and \
                        'type' in problem and \
                        'tags' in problem:

                    # Название задачи
                    name = problem["name"]

                    # Может отсутствовать. Максимальное количество баллов за задачу.
                    if 'points' in problem:
                        points = problem["points"]
                    else:
                        points = 0

                    # Может отсутствовать. Рейтинг задачи (сложность).
                    if 'rating' in problem:
                        rating = problem["rating"]
                    else:
                        rating = 0

                    # буква или буква с цифрой, обозначающие индекс задачи в соревновании.
                    index = problem['index']

                    # Принимает два значения:PROGRAMMING, QUESTION.
                    if 'type' in problem:
                        type = problem["type"]
                    else:
                        type = ""

                    # id соревнования
                    contestId = problem['contestId']

                    # Список тэгов
                    tags = problem['tags']

                    # получаем количество решивших задачу
                    solved_count = self.get_solved_count(problemStatistics, contestId, index)
                    data = {
                        "name": name,
                        "index": index,
                        "points": points,
                        "rating": rating,
                        "contestId": contestId,
                        "type": type,
                        "solved_count": solved_count,
                        "tags": tags,
                    }
                    self.create_problem(data)
                else:
                    print(f"Неправильный формат {problem}")
                    self.save_log(f"Неправильный формат {problem}")

            problems_added = Problems.objects.all().count() - counter_problems
            tags_added = Tags.objects.all().count() - counter_tags
            if problems_added + tags_added > 0:
                text = f"Добавлено {problems_added} задач и {tags_added} тегов"
                print(text)
                self.save_log(text)
        else:
            # Если status равен "FAILED", то поле comment содержит
            # причину, по которой запрос не получилось выполнить
            print(result["comment"])
            self.save_log(result["comment"])

    def create_problem(self, data):
        name = data["name"]
        index = data["index"]
        points = data["points"]
        rating = data["rating"]
        contestId = data["contestId"]
        type_problem = data["type"]
        solved_count = data["solved_count"]
        tags = data["tags"]
        for tag in tags:
            if not Tags.objects.filter(name=tag).exists():
                tag_instanсe = Tags.objects.create(
                    name=tag
                )
            else:
                tag_instanсe = Tags.objects.get(name=tag)

            try:
                problem_instance = Problems.objects.get(contestId=contestId, index=index)
            except Problems.DoesNotExist:
                problem_instance = Problems.objects.create(
                    name=name,
                    contestId=contestId,
                    index=index,
                    points=points,
                    rating=rating,
                    type_problem=type_problem,
                    solved_count=solved_count
                )
                # Проверяем, есть ли уже связь между задачей и тэгом
                if problem_instance not in tag_instanсe.problem.all():
                    tag_instanсe.problem.add(problem_instance)

                # tag_instanse.problem.objects.filter(contestId=contestId, index=index).exists()
            # добавить проверку на существование
            # if not Problems.objects.filter(contestId=contestId, index=index, tags__in=[tag_instanse]).exists():
            #     problem_instanse = tag_instanse.problem.create(
            #         name=name,
            #         index=index,
            #         points=points,
            #         rating=rating,
            #         contestId=contestId,
            #         type_problem=type_problem,
            #         solved_count=solved_count,
            #         tags=tags
            #     )

    def get_solved_count(self, problemstatistics, contestId, index):
        for problemstatistic in problemstatistics:
            if 'contestId' in problemstatistic and \
                'index' in problemstatistic and \
                    'solvedCount' in problemstatistic:
                if problemstatistic['contestId'] == contestId \
                        and problemstatistic['index'] == index:
                    solved_count = problemstatistic['solvedCount']
                    return solved_count
        return 0
