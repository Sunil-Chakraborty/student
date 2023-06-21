from django import forms
from django.forms import Form, ModelForm, DateField, widgets
from .models import Student,Fin_Year

class StudentForm(forms.ModelForm):
    
    class Meta:
        model = Student
        #fields = "__all__"
        exclude = ['year_name','faculty_name','courses_name','email'] 
            
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control skip-enter'})
            field.required = True
                
           
    def get_verbose_name(self, field_name):
        return self.fields[field_name].widget._meta.model._meta.get_field(field_name).verbose_name
