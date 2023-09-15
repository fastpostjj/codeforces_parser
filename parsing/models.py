from django.db import models
from config.settings import NULLABLE, URL_PROBLEM
from user_auth.models import User


class Contest(models.Model):
    """
    Контесты, по которым распределяются задачи
    name,
    annotation
    """

    name = models.CharField(
        max_length=200,
        verbose_name="Название контеста",
    )
    annotation = models.TextField(
        verbose_name="Описание контеста",
        **NULLABLE
    )

    class Meta:
        verbose_name = 'контест'
        verbose_name_plural = 'контесты'

    def __str__(self):
        return f"Уровень {self.name}"


class Problems(models.Model):
    """
    Класс Задачи
    name,
    contestId,
    index,
    points,
    rating,
    type_problem,
    solved_count,
    contest
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

    contest = models.ForeignKey(
        Contest,
        verbose_name="Контест",
        on_delete=models.SET_NULL,
        **NULLABLE
    )

    class Meta:
        verbose_name = 'задача'
        verbose_name_plural = 'задачи'
        unique_together = ("contestId", "index")

    def get_url(self):
        return f"{URL_PROBLEM}{self.contestId}/{self.index}"

    def __str__(self):
        return f"Задача {self.contestId}{self.index} {self.name}. " + \
            f"Сложность: {self.rating}, решений: {self.solved_count}, контест: {self.contest}"


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

    def __str__(self):
        return f"{self.name}"


class Subscriptions(models.Model):
    """
    подписки пользователей
    user,
    contest,
    tag,
    rating,
    is_active
    """
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE
    )

    contest = models.ForeignKey(
        Contest,
        verbose_name="Контест",
        on_delete=models.DO_NOTHING
    )

    tag = models.ForeignKey(
        Tags,
        verbose_name="Тэг",
        on_delete=models.DO_NOTHING
    )

    rating = models.IntegerField(
        default=None,
        verbose_name="уровень сложности",
        **NULLABLE
    )

    is_active = models.BooleanField(
        verbose_name="Активна"
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f"Рассылка задач по теме {self.tag} {self.contest} рейтинг {self.rating if self.rating else '-'}"
