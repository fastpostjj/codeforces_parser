from django.core.management import BaseCommand
from parsing.models import Problems, Tags
from parsing.services.services import GetProblems


class Command(BaseCommand):
    def handle(self, *args, **options):
        # problems = Problems.objects.all().count()
        # tags = Tags.objects.all().count()
        # print(f"Всего задач: {problems}, всего тэгов: {tags}")
        GetProblems.get_problems_by_tag('hashing')
