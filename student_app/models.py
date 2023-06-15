from django.db import models

# Create your models here.

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
    year = models.CharField(verbose_name="Year", max_length=20,null=True, blank=True)
    course_name = models.CharField(verbose_name="Course Name",max_length=100,null=True, blank=True)
    faculty  = models.CharField(verbose_name="Faculty", max_length=50,null=True, blank=True)
    courses  = models.CharField(verbose_name="Courses",max_length=50,null=True, blank=True)    
    intake   = models.IntegerField(verbose_name="Intake", null=True, blank=True)   
    strength = models.IntegerField(verbose_name="Strength", null=True, blank=True)   

    def __str__(self):
        return self.year
