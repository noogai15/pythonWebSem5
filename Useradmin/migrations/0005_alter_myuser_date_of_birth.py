# Generated by Django 3.2.9 on 2021-11-26 12:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Useradmin', '0004_alter_myuser_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='date_of_birth',
            field=models.DateField(default=datetime.date(2001, 11, 26)),
        ),
    ]