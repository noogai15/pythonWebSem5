# Generated by Django 3.1.3 on 2020-11-27 18:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Books', '0003_comment_vote'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='user',
            new_name='myuser',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='user',
            new_name='myuser',
        ),
        migrations.RenameField(
            model_name='vote',
            old_name='user',
            new_name='myuser',
        ),
    ]
