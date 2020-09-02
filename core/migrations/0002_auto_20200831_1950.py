# Generated by Django 3.1 on 2020-08-31 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='volunteer',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='volunteer',
            name='birth_date',
        ),
        migrations.RemoveField(
            model_name='volunteer',
            name='location',
        ),
        migrations.AddField(
            model_name='volunteer',
            name='prompt',
            field=models.TextField(default='a', max_length=2000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='volunteer',
            name='slug',
            field=models.SlugField(default='a', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='volunteer',
            name='title',
            field=models.CharField(default='a', max_length=140),
            preserve_default=False,
        ),
    ]