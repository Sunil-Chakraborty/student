from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.db import models

# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(email, password, **extra_fields)

class Account(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    emp_id = models.CharField(verbose_name="Emp_id", unique=True, max_length=6) 
    Department = models.ForeignKey("Department", on_delete=models.CASCADE, null=True, blank=True)
    dept_name = models.CharField(max_length=100,null=True, blank=True)
    faculty = models.CharField(max_length=50,null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = MyAccountManager()
    
    def has_module_perms(self, app_label):
        """
        Returns True if the user has any permissions in the given app label.
        """
        return self.is_active and self.is_staff

    def has_perm(self, perm, obj=None):
        """
        Returns True if the user has the specified permission. This method
        is used by the Django admin app to determine which users can access
        which parts of the admin interface.
        """
        return self.is_active and self.is_staff
    
    def __str__(self):
        return self.email

class Department(models.Model):
    name = models.CharField(max_length=60, unique=True)
    faculty = models.CharField(max_length=100,  null=True, blank=True)
 
    def __str__(self):
        return self.name




