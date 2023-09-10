from django.core.management import BaseCommand
from parsing.models import Problems, Tags
from parsing.services.services import GetProblems
from parsing.services.codeforces_parser import CodeforcesParser


class Command(BaseCommand):
    def handle(self, *args, **options):
        problems = Problems.objects.all().count()
        tags = Tags.objects.all().count()
        print(f"Всего задач: {problems}, всего тэгов: {tags}")


        # pr = GetProblems.get_problems_by_tag(tag='geometry', rating=800)
        # print(GetProblems.get_all_rating())
        # for p in pr:
        #     print(p, p.get_url())
        parser = CodeforcesParser()
        parser.set_contest_level()
