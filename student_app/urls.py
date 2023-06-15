from django.urls import path

from student_app.views import (
	table_view,
    student_create,
    Chart1,
	)
 
app_name = 'student_app'

urlpatterns = [   
    path('table-view/', table_view, name='table-view'),
    path('student-create/', student_create, name='student-create'),
    path('chart1/', Chart1, name='chart1'),
]