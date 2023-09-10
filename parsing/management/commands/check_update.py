from django.core.management import BaseCommand
from parsing.services.codeforces_parser import CodeforcesParser


class Command(BaseCommand):
    def handle(self, *args, **options):
        conn = CodeforcesParser()
        conn.get_update()
