# Generated by Django 3.1.4 on 2020-12-11 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Useradmin', '0003_auto_20201211_0709'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='type',
            field=models.CharField(choices=[('SU', 'superuser'), ('CS', 'customer service'), ('CU', 'customer'), ('BP', 'business partner')], default='CU', max_length=2),
            preserve_default=False,
        ),
    ]
