# Generated by Django 3.1 on 2020-09-18 22:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_event'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Event',
        ),
    ]