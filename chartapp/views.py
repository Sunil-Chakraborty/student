from django.shortcuts import render
from django.views import View
from student_app.models import Student
from django.db.models import Sum
import matplotlib.pyplot as plt

def ChartView(request):
    
        queryset = Student.objects.values('faculty').annotate(total_intake=Sum('intake'))

        # Prepare the data
        data = [(item['faculty'], int(item['total_intake'])) for item in queryset]

        # Extract the categories and values
        categories = [item[0] for item in data]
        values = [item[1] for item in data]

        # Create the bar plot using Matplotlib
        plt.bar(categories, values)
        plt.xlabel('Faculty')
        plt.ylabel('Total Intake')
        plt.title('Faculty Intake Bar Graph')
        plt.show()

