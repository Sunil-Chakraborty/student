from django.shortcuts import render,redirect
from django.db.models import Q
from django.db.models import Avg,Sum
import matplotlib.pyplot as plt
from io import BytesIO
from django.http import HttpResponse
import numpy as np
from django.forms import modelformset_factory
from django.forms import formset_factory, inlineformset_factory
from .forms import StudentForm
from account.models import Account
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404
from . models import Fin_Year,Courses,Faculty,Student
import pdfplumber

import pytesseract
from PIL import Image
from pdf2image import convert_from_path

import time
import os


# Create your views here.


def is_valid_queryparam(param):
    return param !='' and param is not None

 
def Chart1(request):

    # Bar Chart
    years = [2017, 2018, 2019, 2020, 2021, 2022, 2023]
    tlr_scores = [67.63, 63.57, 51.7, 53.38, 54.4, 57.08, 48.64]
    rp_scores = [53.66, 53.73, 51.72, 52.96, 54.89, 57.07, 54.09]
    go_scores = [90.61, 90.1, 87.77, 90.39, 90.28, 91.39, 91.42]
    oi_scores = [56.79, 56.86, 50.16, 48.67, 44.95, 36, 53.37]
    pear_scores = [58.76, 64.67, 67.31, 71.44, 51.83, 35.5, 28.81]

    plt.figure(figsize=(10, 6))

    # Calculate the width of each bar
    bar_width = 0.15

    # Set the positions of the bars on the x-axis
    r1 = range(len(years))
    r2 = [x + bar_width for x in r1]
    r3 = [x + bar_width for x in r2]
    r4 = [x + bar_width for x in r3]
    r5 = [x + bar_width for x in r4]

    # Plot the bars for each score category
    plt.bar(r1, tlr_scores, color='b', width=bar_width, label='TLR score')
    plt.bar(r2, rp_scores, color='g', width=bar_width, label='RP score')
    plt.bar(r3, go_scores, color='r', width=bar_width, label='GO score')
    plt.bar(r4, oi_scores, color='c', width=bar_width, label='OI score')
    plt.bar(r5, pear_scores, color='m', width=bar_width, label='Pear Perception score')

    # Set the x-axis labels
    plt.xticks([r + bar_width*2 for r in range(len(years))], years)

    plt.xlabel('Year')
    plt.ylabel('Score')
    plt.title('Trends in JU Scores')
    plt.legend()
    plt.grid(True)

    plt.show()
    
     # Save the chart image to a BytesIO object
    chart_image = BytesIO()
    plt.savefig(chart_image, format='png')
    chart_image.seek(0)

    # Create an HttpResponse object with the chart image
    response = HttpResponse(content_type='image/png')
    response['Content-Disposition'] = 'attachment; filename="chart.png"'
    response.write(chart_image.getvalue())

    return response

    
def table_view(request):

    qs=Student.objects.all()
    count = qs.count()

    fin_yr=Fin_Year.objects.all()
    courses=Courses.objects.all()
    faculty=Faculty.objects.all()
      
    years_query = request.GET.getlist('year')    
    course_query=request.GET.getlist('course')
    faculty_query=request.GET.getlist('faculty')
    
    if count > 0 :
        qs=qs.filter(year_name__in=years_query)    
        qs=qs.filter(courses_name__in=course_query)
        qs=qs.filter(faculty_name__in=faculty_query)
        
        qs_sum_intake=qs.aggregate(s=Sum('intake'))["s"]
        
        qs_sum_strength=qs.aggregate(s=Sum('strength'))["s"]
        
        #queryset = Student.objects.values('faculty').annotate(total_intake=Sum('intake'))
        queryset = qs.values('faculty_name').annotate(total_intake=Sum('intake'))
        #queryset = qs.values('faculty_name').annotate(total_intake=Sum('intake'), total_strength=Sum('strength'))
        # Prepare the data for chart view
        data = [(item['faculty_name'], int(item['total_intake'])) for item in queryset]
        #data = [(item['faculty_name'], int(item['total_intake']), int(item['total_strength'])) for item in queryset]
        # Extract the categories and values
        categories = [item[0] for item in data]
        values = [item[1] for item in data]
        
        #intake_values = [item[1] for item in data]
        #strength_values = [item[2] for item in data]
        
        
        context={
            "queryset":qs,
            "fin_yr":fin_yr,
            "courses":courses,
            "faculty":faculty,
            "qs_sum_intake":qs_sum_intake,
            "qs_sum_strength":qs_sum_strength,
            "years_query":years_query,
            "course_query":course_query,
            "faculty_query":faculty_query,
            "categories":categories,
            "values":values,
            #"intake_values":intake_values,
            #"strength_values":strength_values,
        }
        return render(request, "student_app/table_form.html", context)
    else :
        return redirect('dashboard')
    
    
  
def student_create(request,*args, **kwargs):
   
    user_id = request.session['user_id']
    account = Account.objects.get(id=user_id)
    
    if request.method == 'POST':
       
        StudentFormSet = formset_factory(StudentForm, extra=4)
        formset = StudentFormSet(request.POST)
        
        
        if formset.is_valid():
            for form in formset:
                if form.has_changed():                                        
                    user = form.save(commit=False)
                    
                    user.email = account
                    print(account.username)
                    
                    form.save()
            
            #return redirect('dashboard')
            return redirect('student:student-edit')
    else:
       
        StudentFormSet = formset_factory(StudentForm, extra=4)
        formset = StudentFormSet()
        
    context = {
        'formset': formset,
                
    }
    return render(request, 'student_app/student_create.html', context)


def student_edit(request):

    user_id = request.session['user_id']
    account = Account.objects.get(id=user_id)
    
    qs=Student.objects.all()
    #qs=qs.filter(email=account)
    
    
    count = qs.count()
    
    #if count > 0 :
        
        
    context={
        "queryset":qs,
        
    }
    return render(request, "student_app/edit_table_form.html", context)
    #else :
    #    return redirect('dashboard')
        
        
def edit_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_app:student-edit')
    else:
        form = StudentForm(instance=student)

    return render(request, 'student_app/edit_row.html', {'form': form, 'student': student})

def student_delete(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    
    if request.method == "POST":
        student.delete()
        return redirect("student_app:student-edit")
        
    context = {'student':student}
    
    return render(request, 'student_app/student_delete.html', context)

def modal_form(request):
    context={}
    return render(request, "sample_BS_modal.html", context)