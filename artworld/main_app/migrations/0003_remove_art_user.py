# Generated by Django 2.2.6 on 2019-12-20 00:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_art_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='art',
            name='user',
        ),
    ]