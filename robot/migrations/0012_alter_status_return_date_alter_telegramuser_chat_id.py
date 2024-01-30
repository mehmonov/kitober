# Generated by Django 4.1.7 on 2024-01-28 06:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robot', '0011_alter_status_return_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='return_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 7, 11, 4, 53, 921836), editable=False, verbose_name='Kitobni qaytarish muddati'),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='chat_id',
            field=models.IntegerField(),
        ),
    ]
