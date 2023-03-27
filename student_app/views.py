from django.shortcuts import render
from django.db.models import Q
from django.db.models import Avg,Sum


# Create your views here.
from . models import Fin_Year,Courses,Faculty,Student


def is_valid_queryparam(param):
    return param !='' and param is not None
    
def BootstrapFilterView(request):

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
    
    
    context={
        "queryset":qs,
        "fin_yr":fin_yr,
        "courses":courses,
        "faculty":faculty,
        "qs_sum_intake":qs_sum_intake,
        "qs_sum_strength":qs_sum_strength,
    }
    
    return render(request, "bootstrap_form.html", context)
