# Generated by Django 4.1.7 on 2023-08-20 11:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0019_alter_salesitem_belt_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesitem',
            name='quantity',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(450.0)], verbose_name='Quantity(m)'),
        ),
    ]