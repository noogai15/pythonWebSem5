# Generated by Django 3.2.9 on 2021-11-21 12:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Games', '0007_vote_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='comment',
        ),
    ]
