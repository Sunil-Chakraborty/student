# Generated by Django 4.1.7 on 2023-07-02 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='modified_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]