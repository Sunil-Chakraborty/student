# Generated by Django 4.1.7 on 2023-08-04 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_message_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='modified_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
