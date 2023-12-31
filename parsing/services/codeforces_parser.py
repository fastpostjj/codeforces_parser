import requests
import json
from config.settings import URL, LOG_FILE
from django.utils import timezone
from parsing.models import Problems, Tags, Contest


"""
Ответом на каждый запрос является JSON-объект с тремя возможными полями: status,
comment и result.

Статус может быть "OK" или "FAILED".
Если status равен "FAILED", то поле comment содержит причину, по которой запрос
не получилось выполнить. Если status равен "OK", то поле comment отсутствует.
Если status равен "OK", то поле result содержит результат запроса в формате JSON,
который зависит от метода и для каждого метода описан отдельно. Если status равен
"FAILED", то поле result отсутствует.

"""


class CodeforcesParser():
    """
    Класс CodeforcesParser для работы с API сайта https://codeforces.com/,
    на котором размещены задачи
    """

    def __init__(self):
        self._url = URL
        self.log_file_name = LOG_FILE

    def save_log(self, text: str) -> None:
        datetime_now = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file_name, "a", encoding="utf-8") as file:
            file.write(f"{datetime_now} {text}\n")

    @staticmethod
    def get_contest_level(solved: int) -> Contest:
        """
        Метод возвращает уровень контеста в зависимости от сложности задачи.
        Уровень 1
        Задачи, у которых число решений менее 10
        Уровень 2
        Задачи, у которых число решений от 10 до 100
        Уровень 3
        Задачи, у которых число решений от 100 до 500
        Уровень 4
        Задачи, у которых число решений от 500 до 1 000
        Уровень 5
        Задачи, у которых число решений от 1 000 до 10 000
        Уровень 6
        Задачи, у которых число решений от 10 000 до 100 000
        Уровень 7
        Задачи, у которых число решений больше 100 000
        """
        if solved <= 10:
            contest = Contest.objects.get(name="1")
        elif solved <= 100:
            contest = Contest.objects.get(name="2")
        elif solved <= 500:
            contest = Contest.objects.get(name="3")
        elif solved <= 1000:
            contest = Contest.objects.get(name="4")
        elif solved <= 10000:
            contest = Contest.objects.get(name="5")
        elif solved <= 100000:
            contest = Contest.objects.get(name="6")
        else:
            contest = Contest.objects.get(name="7")
        return contest

    def set_contest_level(self) -> None:
        """
        заполнение поля contest у всех объектов Problems,
        у которых это поле не заполено
        """
        problems = Problems.objects.filter(contest__isnull=True)
        for problem in problems:
            solved = problem.solved_count
            problem.contest = self.get_contest_level(solved)
            problem.save()

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url: str):
        self._url = url

    def get_data_from_site(self) -> str | None:
        """
        метод отправляет запрос на сайт и возвращает полученные данные
        """
        method = "problemset.problems"
        try:
            response = requests.get(
                f"{self.url}{method}",
                {
                    "lang": "ru"
                })
        except Exception as error:
            self.save_log(f"Ошибка получения данных {error}")

        if response.status_code == 200:
            if response.json()["status"] == "OK":
                result = response.json()

                # сохраняем полученные данные в файл
                with open("res.json", mode="w", encoding="utf-8") as file:
                    json.dump(result, file)
                return result
            else:
                # comment содержит текст ошибки
                self.save_log(response.json()["comment"])
        else:
            self.save_log(f"Ошибка при выполнении запроса URL={self.url}{method}")

    def get_from_file(self, filename="res.json"):
        with open(filename, mode="r", encoding="utf-8") as file:
            result = json.load(file)
            return result

    def get_data_from_response(self, result):
        """
        разбираем полученные данные и создаем объекты
        """
        if result["status"] == "OK":
            if "problems" in result["result"] and "problemStatistics" in result["result"]:
                problems = result["result"]["problems"]
                problemStatistics = result["result"]["problemStatistics"]
                counter_problems = Problems.objects.all().count()
                counter_tags = Tags.objects.all().count()

                for problem in problems:
                    # Проверяем корректность полученного словаря на наличие обязательных ключей
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
                        contest = self.get_contest_level(solved_count)
                        data = {
                            "name": name,
                            "index": index,
                            "points": points,
                            "rating": rating,
                            "contestId": contestId,
                            "type": type,
                            "solved_count": solved_count,
                            "tags": tags,
                            "contest": contest,
                        }
                        self.create_problem(data)
                    else:
                        self.save_log(f"Неправильный формат {problem}")

                problems_added = Problems.objects.all().count() - counter_problems
                tags_added = Tags.objects.all().count() - counter_tags
                if problems_added + tags_added > 0:
                    text = f"Добавлено {problems_added} задач и {tags_added} тегов"
                    self.save_log(text)
                else:
                    text = "Новых задач и тэгов нет"
                    self.save_log(text)
            else:
                self.save_log("Неправильный формат ответа")

        else:
            # Если status равен "FAILED", то поле comment содержит
            # причину, по которой запрос не получилось выполнить
            self.save_log(result["comment"])

    def get_update(self):
        """
        получаем данные с сайта
        """
        # создаем уровни, если их нет
        self.create_contests()

        self.save_log("check update")
        result = self.get_data_from_site()

        self.get_data_from_response(result)

    def create_contests(self):
        """
        создание уровней
        """
        try:
            Contest.objects.get(name="1")
        except Contest.DoesNotExist:
            Contest.objects.create(
                name="1",
                annotation="Задачи, у которых число решений менее 10"
                                   )
        try:
            Contest.objects.get(name="2")
        except Contest.DoesNotExist:
            Contest.objects.create(
                name="2",
                annotation="Задачи, у которых число решений от 10 до 100"
                )
        try:
            Contest.objects.get(name="3")
        except Contest.DoesNotExist:
            Contest.objects.create(
                name="3",
                annotation="Задачи, у которых число решений от 100 до 500"
                )
        try:
            Contest.objects.get(name="4")
        except Contest.DoesNotExist:
            Contest.objects.create(
                name="4",
                annotation="Задачи, у которых число решений от 500 до 1 000"
                )
        try:
            Contest.objects.get(name="5")
        except Contest.DoesNotExist:
            Contest.objects.create(
                name="5",
                annotation="Задачи, у которых число решений от 1 000 до 10 000"
                )
        try:
            Contest.objects.get(name="6")
        except Contest.DoesNotExist:
            Contest.objects.create(
                name="6",
                annotation="Задачи, у которых число решений от 10 000 до 100 000"
                )
        try:
            Contest.objects.get(name="7")
        except Contest.DoesNotExist:
            Contest.objects.create(
                name="7",
                annotation="Задачи, у которых число решений больше 100 000"
                )

    def update_problem(self, problem_instance, data):
        name = data["name"]
        index = data["index"]
        points = data["points"]
        rating = data["rating"]
        contestId = data["contestId"]
        type_problem = data["type"]
        solved_count = data["solved_count"]
        contest = data["contest"]
        if contestId == problem_instance.contestId and index == problem_instance.index:
            if problem_instance.name != name:
                problem_instance.name = name
            if problem_instance.points != points:
                problem_instance.points = points
            if problem_instance.rating != rating:
                problem_instance.rating = rating
            if problem_instance.type_problem != type_problem:
                problem_instance.type_problem = type_problem
            if problem_instance.solved_count != solved_count:
                problem_instance.solved_count = solved_count
            if problem_instance.contest != contest:
                problem_instance.contest = contest
        return problem_instance

    def create_problem(self, data):
        name = data["name"]
        index = data["index"]
        points = data["points"]
        rating = data["rating"]
        contestId = data["contestId"]
        type_problem = data["type"]
        solved_count = data["solved_count"]
        tags = data["tags"]
        contest = data["contest"]
        for tag in tags:
            # получаем объект тэг или создаем если такого еще нет
            if not Tags.objects.filter(name=tag).exists():
                tag_instanсe = Tags.objects.create(
                    name=tag
                )
            else:
                tag_instanсe = Tags.objects.get(name=tag)

            # получаем или создаем задачу
            try:
                problem_instance = Problems.objects.get(contestId=contestId, index=index)

                # проверяем изменились ли поля задачи кроме contestId и index
                self.update_problem(problem_instance, data)
            except Problems.DoesNotExist:
                problem_instance = Problems.objects.create(
                    name=name,
                    contestId=contestId,
                    index=index,
                    points=points,
                    rating=rating,
                    type_problem=type_problem,
                    solved_count=solved_count,
                    contest=contest
                )
                # Проверяем, есть ли уже связь между задачей и тэгом, если нет - создаем
            if problem_instance and problem_instance not in tag_instanсe.problem.all():
                tag_instanсe.problem.add(problem_instance)
        if not tags or len(tags) == 0:
            # тэгов нет
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
                    solved_count=solved_count,
                    contest=contest
                )
        if problem_instance:
            return problem_instance
        else:
            self.save_log("Ошибка создания задачи ", data)

    def get_solved_count(self, problemstatistics, contestId, index):
        # находим количество решений задачи
        for problemstatistic in problemstatistics:
            if 'contestId' in problemstatistic and \
                'index' in problemstatistic and \
                    'solvedCount' in problemstatistic:
                if problemstatistic['contestId'] == contestId \
                        and problemstatistic['index'] == index:
                    solved_count = problemstatistic['solvedCount']
                    return solved_count
        return 0
