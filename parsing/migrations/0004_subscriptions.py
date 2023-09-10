# Generated by Django 4.2.4 on 2023-09-10 13:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('parsing', '0003_contest_alter_problems_unique_together_botmessages_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(blank=True, default=0, null=True, verbose_name='уровень сложности')),
                ('is_active', models.BooleanField(verbose_name='Активна')),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='parsing.contest', verbose_name='Контест')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='parsing.tags', verbose_name='Тэг')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
    ]
