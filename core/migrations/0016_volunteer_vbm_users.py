# Generated by Django 3.1 on 2020-09-22 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_priority_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteer',
            name='vbm_users',
            field=models.IntegerField(default=0),
        ),
    ]
