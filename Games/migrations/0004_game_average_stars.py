# Generated by Django 3.2.9 on 2021-11-29 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Games', '0003_auto_20211129_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='average_stars',
            field=models.IntegerField(default=0),
        ),
    ]