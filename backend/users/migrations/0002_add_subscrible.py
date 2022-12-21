# Generated by Django 3.2.16 on 2022-12-21 04:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_add_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='subscribe',
            field=models.ManyToManyField(related_name='subscribers', to=settings.AUTH_USER_MODEL, verbose_name='Подписка'),
        ),
    ]
