# Generated by Django 3.1.2 on 2020-10-30 06:13

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('subtitle', models.CharField(blank=True, max_length=100)),
                ('author', models.CharField(max_length=50)),
                ('pages', models.IntegerField()),
                ('date_published', models.DateField(blank=True, default=datetime.date.today)),
                ('type', models.CharField(choices=[('H', 'Hardcover'), ('P', 'Paperback'), ('E', 'E-book'), ('A', 'Audio book')], max_length=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', related_query_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Book',
                'verbose_name_plural': 'Books',
                'ordering': ['title', '-type'],
            },
        ),
    ]
