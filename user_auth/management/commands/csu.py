from django.core.management import BaseCommand
from user_auth.models import User


class Command(BaseCommand):
    """
   Создаем суперпользователя с id 1 и паролем 123abc123
    """

    def create_superuser(self, *args, **options):
        user = User.objects.create(
            chat_id=1,
            email='admin@admin.pro',
            first_name='Admin',
            last_name='SuperAdmin',
            is_staff=True,
            is_superuser=True
        )
        user.set_password('123abc123')
        user.save()

    def change_password(self, *args, **options):
        user = User.objects.get(chat_id=2)
        user.set_password('123abc123')
        user.save()

    def handle(self, *args, **options):
        self.create_superuser(*args, **options)
        # self.change_password(*args, **options)
