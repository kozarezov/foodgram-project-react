# Generated by Django 3.2.16 on 2023-01-10 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_add_uniq'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='favorite',
        ),
    ]