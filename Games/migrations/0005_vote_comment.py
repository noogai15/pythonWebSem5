# Generated by Django 3.2.9 on 2021-11-21 12:35

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Games', '0004_auto_20211121_1233'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='comment',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Games.comment'),
            preserve_default=False,
        ),
    ]
