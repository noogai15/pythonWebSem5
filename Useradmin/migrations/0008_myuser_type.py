# Generated by Django 3.2.9 on 2021-12-03 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Useradmin', '0007_alter_myuser_date_of_birth'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='type',
            field=models.CharField(choices=[('SU', 'superuser'), ('CS', 'customer service'), ('CU', 'customer')], default='CU', max_length=2),
        ),
    ]
