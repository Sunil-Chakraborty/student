# Generated by Django 4.1.7 on 2023-09-07 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0024_alter_salesitem_perprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesitem',
            name='perprice',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Rate (Rs./m)'),
        ),
    ]
