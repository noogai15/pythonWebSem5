# Generated by Django 3.2.9 on 2021-12-05 17:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Useradmin', '0009_auto_20211203_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='date_of_birth',
            field=models.DateField(default=datetime.date(2001, 12, 5)),
        ),
    ]