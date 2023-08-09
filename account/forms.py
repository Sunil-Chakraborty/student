from django import forms
from django.contrib import messages
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.forms import Form, ModelForm, DateField, widgets
from django.contrib.auth.forms import UserCreationForm
from .models import Account, Message


class RegistrationForm(UserCreationForm):
        
    class Meta:
        model = Account
        fields = ('emp_id','email','username','Department','dept_name','password1','password2',
                  'faculty',)

        widgets =  {           
            'emp_id'      : widgets.NumberInput(attrs={
                                'class': 'form-control', 
                                'default': 'blank',                   
                                'oninput': 'limit_input()'
                            }),            
            'username'    : widgets.TextInput(attrs={'class': 'form-control'}),
             
            'Department'  : widgets.Select(attrs={'class': 'form-control','style': 'height:40px;'}),
            'email'       : widgets.TextInput(attrs={'class': 'form-control'}),
            #'Department'  : widgets.Select(attrs={'style': 'width:100%;height:40px;border: 1px solid lightgrey;border-radius: 5px;border-bottom-width: 2px;'}),
            'password1'   : widgets.PasswordInput(attrs={'style': 'width:100%;height:40px;border: 1px solid lightgrey;border-radius: 5px;'}),
            'password2'   : widgets.PasswordInput(attrs={}),
        }
   
		
    
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2


    
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        #if "@jadavpuruniversity.in" not in email:
            #raise forms.ValidationError ("Email must contain @jadavpuruniversity.in!")
        #return email   
        
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)           
        except Account.DoesNotExist:
            return email
		#raise forms.ValidationError('Email "%s" is already in use.' % account)
        raise forms.ValidationError('The above email address is already registered.')
        
        
    def clean_empid(self):
        emp_id = self.cleaned_data['emp_id']
        if Account.objects.filter(emp_id=emp_id).count() > 0:
            raise forms.ValidationError('This emp_id is already  in use.')
        return emp_id
    
        
    def __init__(self, *args, **kwargs):
            super(RegistrationForm,self).__init__(*args, **kwargs)
            self.fields['emp_id'].widget.attrs['placeholder'] = 'Employee Id'                
            self.fields['emp_id'].widget.attrs['autofocus'] = True
            self.fields['username'].widget.attrs['placeholder'] = 'FULL NAME'
            self.fields['email'].widget.attrs['placeholder'] = 'email@gmail.com'            
            self.fields['Department'].empty_label = "Select Department/School"              
            self.fields['Department'].required = True            
            self.fields['faculty'].required = False
            self.fields['password1'].widget.attrs['placeholder'] = 'put your password'
            self.fields['password2'].widget.attrs['placeholder'] = 'confirm password'
            self.fields['password1'].required = False
            self.fields['password2'].required = False


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ['sender','receiver', 'content','feedback']
        
        widgets =  {
            'sender'    : widgets.Select(attrs={'class': 'form-control'}),
            'receiver'  : widgets.Select(attrs={'class': 'form-control'}),
            'content'   : widgets.Textarea(attrs={'class': 'form-control', 'rows': 3 }),           
        }
    
    def __init__(self, *args, **kwargs):
            super(MessageForm,self).__init__(*args, **kwargs)
            self.fields['feedback'].required = False
            self.fields['content'].required = False
            