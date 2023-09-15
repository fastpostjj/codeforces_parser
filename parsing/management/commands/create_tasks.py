from django.core.management import BaseCommand
from django.utils import timezone
from django_celery_beat.models import PeriodicTask, \
    IntervalSchedule


def create_schedule(period='hourly'):
    """
    функция создает расписание для периодических задач
    """
    if period == 'hourly':
        return IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.HOURS,
        )
    elif period == 'daily':
        return IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.DAYS,
        )


def create_periodic_task_sending():
    """
    функция создания периодической задачи запуска ежедневной рассылки
    """

    # Создаем интервал для повтора
    schedule_daily, created = create_schedule('daily')
    start_time = timezone.now()

    if not PeriodicTask.objects.filter(name='send_messages_every_day').exists():
        # Создаем задачу для повторения
        task_sending = PeriodicTask.objects.create(
            interval=schedule_daily,
            name='send_messages_every_day',
            start_time=start_time,
            task='parsing.tasks.send_messages_every_day'
           )
    else:
        task_sending = PeriodicTask.objects.filter(name='send_messages_every_day')
    return task_sending


def create_periodic_task_update():
    """
    функция создания периодической задачи проверки обновлений каждый час
    """
    # Создаем интервал для повтора
    schedule_hourly, created = create_schedule('hourly')
    task_update = PeriodicTask.objects.filter(name='check_update')
    start_time = timezone.now()

    if not PeriodicTask.objects.filter(name='check_update').exists():
        # Создаем задачу для повторения
        task_update = PeriodicTask.objects.create(
            interval=schedule_hourly,
            name='check_update',
            start_time=start_time,
            task='parsing.tasks.check_update',
           )
    else:
        task_update = PeriodicTask.objects.filter(name='check_update')
    return task_update


class Command(BaseCommand):
    def handle(self, *args, **options):

        # создаем периодические задачи
        create_periodic_task_update()
        create_periodic_task_sending()
