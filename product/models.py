from django.db import models
from django.core.validators import MaxValueValidator
from account.models import Account

# Create your models here.

class Grade(models.Model):
    name    = models.CharField(max_length=50)
    skim1   = models.CharField(verbose_name='NN-Skim',max_length=30,null=True, blank=True)
    skim2   = models.CharField(verbose_name='EP-Skim',max_length=30,null=True, blank=True)
    covr1   = models.CharField(verbose_name='NN-Cover',max_length=30,null=True, blank=True)
    covr2   = models.CharField(verbose_name='EP-Cover',max_length=30,null=True, blank=True)
    group   = models.CharField(verbose_name='Group',max_length=30,null=True, blank=True)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    PROD_CHOICES = (
 		 (None, 'Select'),
         ('SCB', 'SCB'),
         ('TCB', 'TCB'),
         ('S-PIPE', 'S-PIPE'),
         ('T-PIPE', 'T-PIPE'),
         
	)
    prod_tag        = models.CharField(verbose_name='Prod-Catg', max_length=7,
	                                  choices=PROD_CHOICES, null=True, blank=True)
    width           = models.IntegerField(verbose_name='Width',validators=[MaxValueValidator(9999)],null=True, blank=True)
    
    FAB_CHOICES = (
 		 (None, 'Select'),
         ('NN', 'NN'),
         ('EP', 'EP'),
	)
    fab_type        = models.CharField(verbose_name='Fab-type', max_length=5,
	                                  choices=FAB_CHOICES, null=True, blank=True)    
    grade           = models.ForeignKey("Grade", verbose_name="Grade", on_delete=models.CASCADE, null=True, blank=True)
    brkr_no         = models.IntegerField(verbose_name='No of Breaker',validators=[MaxValueValidator(9)],null=True, blank=True)  
    brkr_type       = models.CharField(verbose_name='Breaker Type', max_length=25, null=True, blank=True)
    top_cover       = models.DecimalField(verbose_name='Top Cover',max_digits=5,decimal_places=2,null=True,blank=True)
    bot_cover       = models.DecimalField(verbose_name='Top Cover',max_digits=5,decimal_places=2,null=True,blank=True)
    EDGE_CHOICES = (
 		 (None, 'Select'),
         ('CE', 'CE'),
         ('ME', 'ME'),
	)
    edge            = models.CharField(verbose_name='Edge', max_length=5,choices=EDGE_CHOICES, null=True, blank=True)
    ST_CHOICES = (
            (None, 'Select'),
            ('ST 1000','ST 1000'),
            ('ST 1250','ST 1250'),
            ('ST 1400','ST 1400'),
            ('ST 1600','ST 1600'),
            ('ST 1800','ST 1800'),
            ('ST 2000','ST 2000'),
            ('ST 2500','ST 2500'),
            ('ST 2800','ST 2800'),
            ('ST 3150','ST 3150'),
            ('ST 3500','ST 3500'),
            ('ST 4000','ST 4000'),
            ('ST 4500','ST 4500'),
            ('ST 5000','ST 5000'),
            ('ST 5400','ST 5400'),
            ('ST 6300','ST 6300'),
            ('ST 6800','ST 6800'),
            ('ST 7500','ST 7500'),
            ('ST 2250','ST 2250'),
	)
    st_rating       = models.CharField(verbose_name='Strength', max_length=7,choices=ST_CHOICES, null=True, blank=True)
    cord_dia        = models.DecimalField(verbose_name='Cord Dia',max_digits=5,decimal_places=2,null=True,blank=True)
    STCON_CHOICES = (
 		 (None, 'Select'),
         ('7x7', '7x7'),
         ('7x19', '7x19'),
	)
    cord_const      = models.CharField(verbose_name='Cord Const.', max_length=15,choices=STCON_CHOICES, null=True, blank=True)
    pitch           = models.DecimalField(verbose_name='Cord Pitch',max_digits=5,decimal_places=2,null=True,blank=True)
    no_cords        = models.IntegerField(verbose_name='No of Cords',validators=[MaxValueValidator(99)],null=True, blank=True)
    sensor_loop     = models.IntegerField(verbose_name='Sensor Loop',validators=[MaxValueValidator(9)],null=True, blank=True)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)
    email 	        = models.ForeignKey(Account,verbose_name="email key", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.prod_tag
        
