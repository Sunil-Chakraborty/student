from django.db import models
from django.utils import timezone
from account.models import Account

class Fin_Year(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Courses(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Faculty(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Criteria(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Student(models.Model):
    year            = models.ForeignKey("Fin_Year", verbose_name="Fin Year", on_delete=models.CASCADE, null=True, blank=True)
    course_name     = models.CharField(verbose_name="Course Name", max_length=100, null=True, blank=True)
    faculty         = models.ForeignKey("Faculty", verbose_name="Faculty", on_delete=models.CASCADE, null=True, blank=True)
    courses         = models.ForeignKey("Courses", verbose_name="Courses", on_delete=models.CASCADE, null=True, blank=True)
    intake          = models.IntegerField(verbose_name="Intake", null=True, blank=True)
    strength        = models.IntegerField(verbose_name="Strength", null=True, blank=True)
    year_name       = models.CharField(max_length=30)
    faculty_name    = models.CharField(max_length=12)
    courses_name    = models.CharField(max_length=30)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)
    email 	        = models.ForeignKey(Account,verbose_name="email key", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.year.name

    def save(self, *args, **kwargs):
        if self.year:
            self.year_name = self.year.name
        if self.faculty:
            self.faculty_name = self.faculty.name
        if self.courses:
            self.courses_name = self.courses.name        
        super().save(*args, **kwargs)
        