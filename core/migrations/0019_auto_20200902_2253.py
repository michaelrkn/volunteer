# Generated by Django 3.1 on 2020-09-02 22:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20200902_2045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friend',
            name='email',
        ),
        migrations.RemoveField(
            model_name='friend',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='volunteer',
            name='prompt',
        ),
        migrations.RemoveField(
            model_name='volunteer',
            name='title',
        ),
        migrations.AddField(
            model_name='volunteer',
            name='can_text',
            field=models.BooleanField(default=False, verbose_name='Can we text you at this number?'),
        ),
        migrations.AlterField(
            model_name='friend',
            name='city',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='friend',
            name='first_name',
            field=models.CharField(blank=True, max_length=100, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='friend',
            name='last_name',
            field=models.CharField(blank=True, max_length=100, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='friend',
            name='state',
            field=models.CharField(blank=True, max_length=2),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='phone',
            field=models.CharField(default=1234567890, help_text='Use the same phone number that you used to register your Outvote account, if you have one', max_length=10, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '1234567890'. Up to 10 digits allowed.", regex='^\\d{10}$')]),
            preserve_default=False,
        ),
    ]
