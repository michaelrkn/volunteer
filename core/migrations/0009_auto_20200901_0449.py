# Generated by Django 3.1 on 2020-09-01 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20200901_0432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteer',
            name='slug',
            field=models.SlugField(max_length=30, null=True, unique=True),
        ),
    ]
