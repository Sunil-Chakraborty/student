# Generated by Django 4.1.7 on 2023-06-25 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_product_prod_des'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
