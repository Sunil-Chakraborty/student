# Generated by Django 4.1.7 on 2023-06-18 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_app', '0003_alter_student_faculty_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='faculty_name',
            field=models.CharField(max_length=12),
        ),
    ]
