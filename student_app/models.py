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
    year = models.CharField(max_length=20,null=True, blank=True)
    course_name = models.CharField(max_length=100,null=True, blank=True)
    faculty  = models.CharField(max_length=50,null=True, blank=True)
    courses  = models.CharField(max_length=50,null=True, blank=True)    
    intake   = models.IntegerField(null=True, blank=True)   
    strength = models.IntegerField(null=True, blank=True)   

    def __str__(self):
        return self.year
