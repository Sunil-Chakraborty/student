from django.shortcuts import render
from django.db.models import Q
from django.db.models import Avg,Sum
import matplotlib.pyplot as plt
import numpy as np
import threading
import time


# Create your views here.
from . models import Fin_Year,Courses,Faculty,Student


def is_valid_queryparam(param):
    return param !='' and param is not None


def plot_graph(categories, values):
    # Create the bar plot using Matplotlib
    plt.bar(categories, values)
    for i, v in enumerate(values):
        plt.text(i, v, str(v), ha='center', va='bottom')
    plt.xlabel('Faculty')
    plt.ylabel('Total Intake')
    plt.title('Faculty Intake Bar Graph')
    plt.show()


    
def BootstrapFilterView(request):

    qs=Student.objects.all()
    fin_yr=Fin_Year.objects.all()
    courses=Courses.objects.all()
    faculty=Faculty.objects.all()
      
    years_query = request.GET.getlist('year')    
    course_query=request.GET.getlist('course')
    faculty_query=request.GET.getlist('faculty')
    graph = request.GET.getlist('graph')
    
    
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
    
    if graph :        
        # Create a separate thread to display the plot
        graph_thread = threading.Thread(target=plot_graph, args=(categories, values))
        graph_thread.start()        
    
    
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
    }
    
    return render(request, "bootstrap_form.html", context)
    
