# Generated by Django 3.1 on 2020-09-03 19:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200903_1900'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='volunteer',
            name='can_text',
        ),
        migrations.RemoveField(
            model_name='volunteer',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='volunteer',
            name='zip_code',
        ),
    ]