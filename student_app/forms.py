from django import forms
from django.forms import Form, ModelForm, DateField, widgets
from .models import Student,Fin_Year

class StudentForm(forms.ModelForm):
    
    class Meta:
        model = Student
        #fields = "__all__"
        exclude = ['year_name','faculty_name','courses_name'] 
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control skip-enter'})
            if not self.instance.pk:  # Check if the form is for a new instance
                field.required = True  # Set required attribute to True for non-blank rows
    
    def get_verbose_name(self, field_name):
        return self.fields[field_name].widget._meta.model._meta.get_field(field_name).verbose_name
    
    """       
    def clean(self):
        cleaned_data = super().clean()
        
        year_value = cleaned_data.get('year')
        course_name_value = cleaned_data.get('course_name')
        faculty_value = cleaned_data.get('faculty')
        courses_value = cleaned_data.get('courses')
        intake_value = cleaned_data.get('intake')
        strength_value = cleaned_data.get('strength')
                
        if year_value and year_value !="":
            if not cleaned_data.get('course_name'):
                self.add_error('course_name', 'Course_name is required.')
            if not cleaned_data.get('faculty'):
                self.add_error('faculty', 'Faculty is required.')
            if not cleaned_data.get('courses'):
                self.add_error('courses', 'Courses is required.')
            if not cleaned_data.get('intake'):
                self.add_error('intake', 'Intake is required.')
            if not cleaned_data.get('strength'):
                self.add_error('strength', 'Strength is required.')
        elif course_name_value and course_name_value !="":
            if not cleaned_data.get('year'):
                self.add_error('year', 'Year is required.')
            if not cleaned_data.get('faculty'):
                self.add_error('faculty', 'Faculty is required.')
            if not cleaned_data.get('courses'):
                self.add_error('courses', 'Courses is required.')
            if not cleaned_data.get('intake'):
                self.add_error('intake', 'Intake is required.')
            if not cleaned_data.get('strength'):
                self.add_error('strength', 'Strength is required.')
        elif faculty_value and faculty_value !="":
            if not cleaned_data.get('year'):
                self.add_error('year', 'Year is required.')
            if not cleaned_data.get('course_name'):
                self.add_error('course_name', 'Course_name is required.')
            if not cleaned_data.get('courses'):
                self.add_error('courses', 'Courses is required.')
            if not cleaned_data.get('intake'):
                self.add_error('intake', 'Intake is required.')
            if not cleaned_data.get('strength'):
                self.add_error('strength', 'Strength is required.')
        elif courses_value and courses_value !="":
            if not cleaned_data.get('year'):
                self.add_error('year', 'Year is required.')
            if not cleaned_data.get('course_name'):
                self.add_error('course_name', 'Course_name is required.')
            if not cleaned_data.get('faculty'):
                self.add_error('faculty', 'Faculty is required.')
            if not cleaned_data.get('intake'):
                self.add_error('intake', 'Intake is required.')
            if not cleaned_data.get('strength'):
                self.add_error('strength', 'Strength is required.')
        elif intake_value and intake_value > 0:
            if not cleaned_data.get('year'):
                self.add_error('year', 'Year is required.')
            if not cleaned_data.get('course_name'):
                self.add_error('course_name', 'Course_name is required.')
            if not cleaned_data.get('faculty'):
                self.add_error('faculty', 'Faculty is required.')
            if not cleaned_data.get('courses'):
                self.add_error('courses', 'Courses is required.')
            if not cleaned_data.get('strength'):
                self.add_error('strength', 'Strength is required.')
        elif strength_value and strength_value > 0:
            if not cleaned_data.get('year'):
                self.add_error('year', 'Year is required.')
            if not cleaned_data.get('course_name'):
                self.add_error('course_name', 'Course_name is required.')
            if not cleaned_data.get('faculty'):
                self.add_error('faculty', 'Faculty is required.')
            if not cleaned_data.get('courses'):
                self.add_error('courses', 'Courses is required.')
            if not cleaned_data.get('intake'):
                self.add_error('intake', 'Intake is required.')

        return cleaned_data
    """
    
    