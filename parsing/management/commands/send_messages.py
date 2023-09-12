from django.core.management import BaseCommand
from parsing.services.message_creator import send_messages


class Command(BaseCommand):
    def handle(self, *args, **options):
        send_messages()
