# Generated by Django 4.1.7 on 2023-07-21 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_rename_email_stock_fk_email_alter_stock_br_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='belt_no',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='Belt No'),
        ),
    ]
