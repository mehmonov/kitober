# Generated by Django 4.1.7 on 2024-01-24 07:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='return_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 3, 12, 21, 46, 401346), editable=False, verbose_name='Kitobni qaytarish muddati'),
        ),
    ]
