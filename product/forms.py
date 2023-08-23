from django import forms
from django.forms import Form, ModelForm, DateField, widgets,ValidationError
from .models import Product, Customer, SalesBill, SalesItem, Stock
from django.core.validators import MaxValueValidator
from django.forms import formset_factory
from django.forms import DateInput
from django.urls import reverse_lazy

class ProductTCBForm(forms.ModelForm):
    
    class Meta:
        model = Product
        #fields = "__all__"
        exclude = ['email','prod_code','prod_tag','prod_des','st_rating','cord_dia','cord_const','sensor_loop','pitch','no_cords'] 
       

        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control skip-enter'})
            field.required = True
    
    """        
        self.fields['brkr_no'].required = False    
        self.fields['brkr_type'].required = False
       
        
    def clean(self):
        cleaned_data = super().clean()
        brkr_no_value = cleaned_data.get('brkr_no')

        if brkr_no_value:
            brkr_type_value = cleaned_data.get('brkr_type')
            if not brkr_type_value:
                self.add_error('brkr_type', 'Breaker Type is required when No of Breaker is not empty.')

        return cleaned_data       
    """
    
    def get_verbose_name(self, field_name):
        return self.fields[field_name].widget._meta.model._meta.get_field(field_name).verbose_name


class ProductSCBForm(forms.ModelForm):
    
    class Meta:
        model = Product
        #fields = "__all__"
        exclude = ['email','prod_tag','fab_type','edge','prod_des'] 
            
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control skip-enter'})
            field.required = True
                
           
    def get_verbose_name(self, field_name):
        return self.fields[field_name].widget._meta.model._meta.get_field(field_name).verbose_name


class CustomerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['name'].widget.attrs.update({
            'class': 'textinput form-control',            
            'pattern': '^(?!\\s*$)[a-zA-Z\s]{1,50}$',
            'title': 'Alphabets alongwith Spaces only',
            'required': 'required'  # Add this line to make the field required
        })
       
        
        self.fields['phone'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '10', 'pattern' : '[0-9]{10}', 'title' : 'Numbers only'})
        self.fields['email'].widget.attrs.update({'class': 'textinput form-control'})
        #self.fields['gstin'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '15', 'pattern' : '[A-Z0-9]{15}', 'title' : 'GSTIN Format Required'})
    
    
    def clean_address(self):
        address = self.cleaned_data.get('address')
        if address and address.strip() == '':
            raise forms.ValidationError("Address field cannot be empty or consist only of spaces.")
        return address
        
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'address', 'email']
        widgets = {
            'address' : forms.Textarea(
                attrs = {
                    'class' : 'textinput form-control',
                    'rows'  : '4'
                }
            )
        }

class SelectCustomerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].queryset = Customer.objects.filter(is_deleted=False)
        self.fields['customer'].widget.attrs.update({'class': 'textinput form-control'})
    class Meta:
        model = SalesBill
        fields = ['customer']

class SalesItemForm(forms.ModelForm):
    item_text_content = forms.CharField(required=False)
    item_qty_content = forms.CharField(required=False)
   
    class Meta:
        model = SalesItem
        fields = ['stock', 'quantity', 'perprice', 'item_text_content','item_qty_content']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            field.required = False
         
            
    def get_verbose_name(self, field_name):
        return self.fields[field_name].widget._meta.model._meta.get_field(field_name).verbose_name

    def clean_stock(self):
        stock_instance = self.cleaned_data['stock']
        print("Selected Stock Instance:", stock_instance)
        if stock_instance:
            stock_data = Stock.objects.filter(pk=stock_instance.pk).values('item_text','quantity').first()
            item_des = stock_data['item_text'] if stock_data else ''
            print("Stock Data:", stock_data)
            item_text_content = stock_data['item_text'] if stock_data else ''
            print("Setting item_text_content to:", item_text_content)
            self.cleaned_data['item_text_content'] = item_text_content  # Assign the value to cleaned_data instead of self.instance
            item_qty_content = stock_data['quantity'] if stock_data else ''
            print("Setting item_qty_content to:", item_qty_content)
            self.cleaned_data['item_qty_content'] = item_qty_content  # Assign the value to cleaned_data instead of self.instance
            
        return stock_instance

SalesItemFormset = formset_factory(SalesItemForm, extra=3)
          
    

class StockForm(forms.ModelForm):

       
    class Meta:
        model = Stock
        #fields = "__all__"
        exclude = ['fk_email', 'item_text', 'name','is_deleted', 'created_date', 'modified_date', 'id']
        
        widgets = {
            'doc_no'    :  widgets.TextInput(attrs={'class': 'form-control','style': 'text-transform:uppercase'}),
            'doc_dt'    :  widgets.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'belt_no'   :  widgets.TextInput(attrs={'class': 'form-control','style': 'text-transform:uppercase'}),
            'width'     :  widgets.TextInput(attrs={'class': 'form-control','size':4, 'maxlength':4,'title': 'Numbers only'}),         
            'ply'       :  widgets.TextInput(attrs={'class': 'form-control','size':1, 'maxlength':1,'title': 'Numbers only'}),
            'tr'        :  widgets.TextInput(attrs={'class': 'form-control','size':5, 'maxlength':5,'title': 'Numbers only'}),
            'br'        :  widgets.TextInput(attrs={'class': 'form-control','size':5, 'maxlength':5,'title': 'Numbers only'}),
            'quantity'  :  widgets.TextInput(attrs={'class': 'form-control','size':6, 'maxlength':6,'title': 'Numbers only'}),
        
        }
    
    
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control skip-enter'})
            field.required = True

    
        
    def get_verbose_name(self, field_name):
        return self.fields[field_name].widget._meta.model._meta.get_field(field_name).verbose_name
