from django.core.management import BaseCommand
from parsing.models import Problems, Tags


class Command(BaseCommand):
    def handle(self, *args, **options):
        problems = Problems.objects.all().count()
        tags = Tags.objects.all().count()
        print(f"Всего задач: {problems}, всего тэгов: {tags}")
