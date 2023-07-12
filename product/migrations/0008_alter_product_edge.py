# Generated by Django 4.1.7 on 2023-06-25 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_alter_product_edge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='edge',
            field=models.CharField(blank=True, choices=[(None, 'Select'), ('CE', 'CE'), ('ME', 'ME')], max_length=5, null=True, verbose_name='Edge'),
        ),
    ]