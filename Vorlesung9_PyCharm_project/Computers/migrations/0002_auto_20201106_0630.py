# Generated by Django 3.1.3 on 2020-11-06 05:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Computers', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='computer',
            options={'ordering': ['type', 'brand', 'serial_number'], 'verbose_name': 'Computer', 'verbose_name_plural': 'Computers'},
        ),
    ]
