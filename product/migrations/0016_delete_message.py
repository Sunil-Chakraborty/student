# Generated by Django 4.1.7 on 2023-08-03 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_message'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Message',
        ),
    ]