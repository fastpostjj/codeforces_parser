from django.db import models
from config.settings import NULLABLE, URL_PROBLEM
from user_auth.models import User


class Problems(models.Model):
    """
    Класс Задачи
    name,
    contestId,
    index,
    points,
    rating,
    type,
    solved_count
    """
    name = models.CharField(
        verbose_name="Название задачи",
        max_length=200,
        **NULLABLE
        )

    # Id соревнования, содержащего задачу.
    contestId = models.IntegerField(
        verbose_name="Id соревнования",
        )

    # буква или буква с цифрой, обозначающие индекс задачи в соревновании
    index = models.CharField(
        verbose_name="Индекс задачи",
        max_length=10,
        )

    points = models.IntegerField(
        verbose_name="Максимальное количество баллов за задачу",
        **NULLABLE
        )

    rating = models.IntegerField(
        verbose_name="Рейтинг задачи (сложность)",
        **NULLABLE
        )

    # Принимает два значения:PROGRAMMING, QUESTION
    type_problem = models.CharField(
        verbose_name="Тип задачи",
        max_length=200,
        **NULLABLE
        )

    solved_count = models.IntegerField(
        verbose_name="Число решений задачи",
        **NULLABLE
        )

    class Meta:
        verbose_name = 'задача'
        verbose_name_plural = 'задачи'

    def get_url(self):
        return f"{URL_PROBLEM}{self.contestId}/{self.index}"

    def __str__(self):
        return f"Задача {self.contestId}{self.index} {self.name}. " + \
            f"Сложность: {self.rating}, решений: {self.solved_count}"


class Tags(models.Model):
    """
    Тэги задач
    """
    name = models.CharField(
        verbose_name="Тэг",
        max_length=100,
        unique=True
    )

    problem = models.ManyToManyField(
        Problems,
        verbose_name="Задача"
    )

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'тэги'

    # def __str__(self):
    #     print("***", self.problem, "\n")
    #     return f"{self.name} {self.problem.all()}"
    def __str__(self):
        problems_str = ", ".join([str(problem) for problem in self.problem.all()])
        return f"{self.name} ({problems_str})"


class SendedProblems(models.Model):
    """
    отправленные пользователю задачи
    """
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE
    )

    problem = models.ForeignKey(
        Problems,
        verbose_name="Проблема",
        on_delete=models.CASCADE
    )

    datetimesend = models.DateTimeField(
        verbose_name="Дата и время отправки"
    )

    class Meta:
        verbose_name = 'отправленная задача'
        verbose_name_plural = 'отправленные задачи'

    def __str__(self):
        return f"{self.user} {self.problem} {self.datetimesend}"
