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


import time


# Create your views here.
from . models import Fin_Year,Courses,Faculty,Student
from student_app.models import Student

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
    
    """
    #Multiple Year pie chart in one frame
    years = [2017, 2018, 2019, 2020, 2021, 2022, 2023]
    tlr_scores = [67.63, 63.57, 51.7, 53.38, 54.4, 57.08, 48.64]
    rp_scores = [53.66, 53.73, 51.72, 52.96, 54.89, 57.07, 54.09]
    go_scores = [90.61, 90.1, 87.77, 90.39, 90.28, 91.39, 91.42]
    oi_scores = [56.79, 56.86, 50.16, 48.67, 44.95, 36, 53.37]
    pear_scores = [58.76, 64.67, 67.31, 71.44, 51.83, 35.5, 28.81]
   
    num_years = len(years)
    num_cols = 3
    num_rows = (num_years + num_cols - 1) // num_cols

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 10))
    fig.suptitle('Scores for Different Years\n')

    for i, year in enumerate(years):
        row = i // num_cols
        col = i % num_cols

        scores = [tlr_scores[i], rp_scores[i], go_scores[i], oi_scores[i], pear_scores[i]]
        labels = ['TLR score', 'RP score', 'GO score', 'OI score', 'Pear Perception score']

        axes[row, col].pie(scores, labels=labels, autopct='%1.1f%%')
        axes[row, col].set_title(f'Year {year}')

    plt.tight_layout()
    plt.show()
    
    #Multiple Year pie chart
    years = [2017, 2018, 2019, 2020, 2021, 2022, 2023]
    tlr_scores = [67.63, 63.57, 51.7, 53.38, 54.4, 57.08, 48.64]
    rp_scores = [53.66, 53.73, 51.72, 52.96, 54.89, 57.07, 54.09]
    go_scores = [90.61, 90.1, 87.77, 90.39, 90.28, 91.39, 91.42]
    oi_scores = [56.79, 56.86, 50.16, 48.67, 44.95, 36, 53.37]
    pear_scores = [58.76, 64.67, 67.31, 71.44, 51.83, 35.5, 28.81]
   
    for i, year in enumerate(years):
        scores = [tlr_scores[i], rp_scores[i], go_scores[i], oi_scores[i], pear_scores[i]]
        labels = ['TLR score', 'RP score', 'GO score', 'OI score', 'Pear Perception score']

        plt.figure(figsize=(8, 7))
        plt.pie(scores, labels=labels, autopct='%1.1f%%')
        plt.title(f'Scores for the year {year}')

        plt.show()

    
    Single Year pie chart
    years = [2017, 2018, 2019, 2020, 2021, 2022, 2023]
    tlr_scores = [67.63, 63.57, 51.7, 53.38, 54.4, 57.08, 48.64]
    rp_scores = [53.66, 53.73, 51.72, 52.96, 54.89, 57.07, 54.09]
    go_scores = [90.61, 90.1, 87.77, 90.39, 90.28, 91.39, 91.42]
    oi_scores = [56.79, 56.86, 50.16, 48.67, 44.95, 36, 53.37]
    pear_scores = [58.76, 64.67, 67.31, 71.44, 51.83, 35.5, 28.81]
   
    selected_year = 2023
    selected_index = years.index(selected_year)
    
    scores = [tlr_scores[selected_index], rp_scores[selected_index], go_scores[selected_index],
              oi_scores[selected_index], pear_scores[selected_index]]
    labels = ['TLR score', 'RP score', 'GO score', 'OI score', 'Pear Perception score']
    
    plt.figure(figsize=(8, 7))
    plt.pie(scores, labels=labels, autopct='%1.1f%%')
    plt.title(f'Scores for the year {selected_year}')
    
    plt.show()
    """
    

    
def table_view(request):

    qs=Student.objects.all()
    fin_yr=Fin_Year.objects.all()
    courses=Courses.objects.all()
    faculty=Faculty.objects.all()
      
    years_query = request.GET.getlist('year')    
    course_query=request.GET.getlist('course')
    faculty_query=request.GET.getlist('faculty')
    
    
    qs=qs.filter(year__in=years_query)    
    qs=qs.filter(courses__in=course_query)
    qs=qs.filter(faculty__in=faculty_query)
    
    qs_sum_intake=qs.aggregate(s=Sum('intake'))["s"]
    
    qs_sum_strength=qs.aggregate(s=Sum('strength'))["s"]
    
    #queryset = Student.objects.values('faculty').annotate(total_intake=Sum('intake'))
    queryset = qs.values('faculty').annotate(total_intake=Sum('intake'))
    # Prepare the data for chart view
    data = [(item['faculty'], int(item['total_intake'])) for item in queryset]
    # Extract the categories and values
    categories = [item[0] for item in data]
    values = [item[1] for item in data]
    
    
    
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
    }
    
    
    return render(request, "student_app/table_form.html", context)
    
def student_create(request):   
   
       
    if request.method == 'POST':
       
        StudentFormSet = formset_factory(StudentForm, extra=4)
        formset = StudentFormSet(request.POST)
        
        
        if formset.is_valid():
            for form in formset:
                if form.has_changed(): 
                    form.save()
            
            return redirect('dashboard')
    else:
       
        StudentFormSet = formset_factory(StudentForm, extra=4)
        formset = StudentFormSet()
        
    context = {
        'formset': formset,
                
    }
    return render(request, 'student_app/student_create.html', context)
