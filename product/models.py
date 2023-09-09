from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from account.models import Account
from datetime import datetime
from django.utils import timezone

# Create your models here.

class Grade(models.Model):
    name    = models.CharField(max_length=50,null=True, blank=True)
    skim1   = models.CharField(verbose_name='NN-Skim',max_length=30,null=True, blank=True)
    skim2   = models.CharField(verbose_name='EP-Skim',max_length=30,null=True, blank=True)
    covr1   = models.CharField(verbose_name='NN-Cover',max_length=30,null=True, blank=True)
    covr2   = models.CharField(verbose_name='EP-Cover',max_length=30,null=True, blank=True)
    group   = models.CharField(verbose_name='Group',max_length=30,null=True, blank=True)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    prod_code = models.CharField(verbose_name='Prod-Code', max_length=10, unique=True, null=True, blank=True)
    PROD_CHOICES    = (
 		 (None, 'Select'),
         ('01', 'SCB'),
         ('02', 'TCB'),
         ('03', 'S-PIPE'),
         ('04', 'T-PIPE'),
         
	)
    prod_tag        = models.CharField(verbose_name='Prod-Catg', max_length=7,
	                                  choices=PROD_CHOICES, null=True, blank=True)
       
    FAB_CHOICES     = (
 		 (None, 'Select'),
         ('01', 'NN'),
         ('02', 'EP'),
         ('03', 'PP'),
	)
    fab_type        = models.CharField(verbose_name='Fab-type', max_length=5,
	                                  choices=FAB_CHOICES, null=True, blank=True)    
    
    FAB_DSG  = (
         (None, 'Select'),
         ('01', '90'),
         ('02', '100'),
         ('03', '125'),
         ('04', '160'),
         ('05', '200'),
         ('06', '250'),
         ('07', '315'),
         ('08', '350'),
         ('09', '400'),
         ('10', '450'),
         ('11', '500'),    
    )
    fab_str         = models.CharField(verbose_name='Fab-Style', max_length=3,
	                                  choices=FAB_DSG, null=True, blank=True)
                                      
    grade           = models.ForeignKey("Grade", verbose_name="Grade", on_delete=models.CASCADE, null=True, blank=True)
    
    EDGE_CHOICES = (
 		 (None, 'Select'),
         ('01', 'CE'),
         ('02', 'ME'),
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
    STCON_CHOICES   = (
 		 (None, 'Select'),
         ('01', '7x7'),
         ('02', '7x19'),
	)
    cord_const      = models.CharField(verbose_name='Cord Const.', max_length=15,choices=STCON_CHOICES, null=True, blank=True)
    prod_des        = models.CharField(verbose_name='Item Description', max_length=250, null=True, blank=True)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)
    email 	        = models.ForeignKey(Account,verbose_name="email key", on_delete=models.CASCADE, null=True, blank=True)
    
        
    def __str__(self):
        return f'{self.prod_des}'
        #return f'{self.prod_code} - {self.prod_des}'
        #return f'{self.prod_code}'
        
class Customer(models.Model):
    id              = models.AutoField(primary_key=True)
    name            = models.CharField(verbose_name='Name',max_length=150,null=True, blank=True)
    phone           = models.CharField(verbose_name='Phone',max_length=12, unique=True)
    address         = models.CharField(verbose_name='Address',max_length=200,null=True)
    email           = models.EmailField(verbose_name='Email',max_length=50, unique=True)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)
    fk_email 	    = models.ForeignKey(Account,verbose_name="email key", on_delete=models.CASCADE, null=True, blank=True)
    is_deleted      = models.BooleanField(default=False)

    def __str__(self):
	    return self.name
    

#contains the sales bills made
class SalesBill(models.Model):
    billno = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now=True)
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE, related_name='salescustomer')

    def __str__(self):
	    return "Bill no: " + str(self.billno)

    def get_items_list(self):
        return SalesItem.objects.filter(billno=self)

    def get_total_price(self):
        salesitems = SalesItem.objects.filter(billno=self)
        total = 0
        for item in salesitems:
            total += item.totalprice
        return total


class Stock(models.Model):
    id              = models.AutoField(primary_key=True)    
    doc_no          = models.CharField(verbose_name='Doc.No.', max_length=20, null=True, blank=True)
    doc_dt          = models.DateField(verbose_name='Doc.Date', null=True, blank=True)
    belt_no         = models.CharField(verbose_name='Belt No', max_length=20, unique=True, null=True, blank=True)
    name            = models.CharField(verbose_name='Item Code', max_length=10, null=True, blank=True)
    prod_des        = models.ForeignKey(Product, on_delete = models.CASCADE, related_name='proddesc')    
    item_text       = models.CharField(verbose_name='Item Description', max_length=100, null=True, blank=True)
    width           = models.IntegerField(verbose_name='Width(mm)',validators=[MinValueValidator(500), MaxValueValidator(1800)],null=True, blank=True)
    ply             = models.IntegerField(verbose_name='Ply(no)',validators=[MinValueValidator(2), MaxValueValidator(8)],null=True, blank=True)
    tr              = models.DecimalField(verbose_name='Top Rubber(mm)',validators=[MinValueValidator(1.5), MaxValueValidator(20.00)],max_digits=5, decimal_places=2,null=True,blank=True)
    br              = models.DecimalField(verbose_name='Bot Rubber(mm)',validators=[MinValueValidator(1.5), MaxValueValidator(20.00)],max_digits=5, decimal_places=2,null=True,blank=True)
    quantity        = models.DecimalField(verbose_name='Quantity(m)',validators=[MinValueValidator(10), MaxValueValidator(450.00)],max_digits=6, decimal_places=2,null=True,blank=True)
    is_deleted      = models.BooleanField(default=False)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)
    fk_email 	    = models.ForeignKey(Account,verbose_name="email key", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
	    return self.belt_no
        #return f'{self.belt_no} - {self.prod_des}'
        
        #return f'{self.item_text} - ({self.width}x{self.ply}x{self.tr}x{self.br})'
        #return f'{self.item_text} - ({self.width}x{self.ply}x{self.tr}x{self.br})'
        
#contains the sales stocks made
class SalesItem(models.Model):
    stock               = models.ForeignKey(Stock, on_delete = models.CASCADE, related_name='salesitem')
    belt_no             = models.CharField(verbose_name='Belt No', max_length=20, unique=True, null=True, blank=True)
    prod_des            = models.CharField(verbose_name='Item Description', max_length=250, null=True, blank=True)
    item_text_content   = models.CharField(verbose_name='Item Des', max_length=250)    
    item_qty_content    = models.CharField(verbose_name='Item Qnty', max_length=250)    
    quantity            = models.DecimalField(verbose_name='Quantity(m)',validators=[MinValueValidator(10), MaxValueValidator(450.00)],max_digits=6, decimal_places=2,null=True,blank=True)
    perprice            = models.DecimalField(verbose_name='Rate (Rs./m)',max_digits=6, decimal_places=2,validators=[MinValueValidator(0.01)],null=True,blank=True)
    totalprice          = models.DecimalField(verbose_name='Total(Rs./m)',max_digits=10, decimal_places=2,null=True,blank=True)

    def __str__(self):
	    return self.stock.name
    
class SalesBillDetails(models.Model):
    billno = models.ForeignKey(SalesBill, on_delete = models.CASCADE, related_name='purchasedetailsbillno')
    
    eway = models.CharField(max_length=50, blank=True, null=True)    
    veh = models.CharField(max_length=50, blank=True, null=True)
    destination = models.CharField(max_length=50, blank=True, null=True)
    po = models.CharField(max_length=50, blank=True, null=True)
    
    cgst = models.CharField(max_length=50, blank=True, null=True)
    sgst = models.CharField(max_length=50, blank=True, null=True)
    igst = models.CharField(max_length=50, blank=True, null=True)
    cess = models.CharField(max_length=50, blank=True, null=True)
    tcs = models.CharField(max_length=50, blank=True, null=True)
    total = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
	    return "Bill no: " + str(self.billno.billno)

      