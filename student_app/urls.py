from django.urls import path

from student_app.views import (
	table_view,
    student_create,
    student_edit,
    edit_student,
    student_delete,
    Chart1,
	)
 
app_name = 'student_app'

urlpatterns = [   
    path('table-view/', table_view, name='table-view'),
    path('student-create/', student_create, name='student-create'),
    path('student-edit/', student_edit, name='student-edit'),
    path('edit/<int:student_id>/', edit_student, name='edit-student'),
    path('delete/<int:student_id>/', student_delete, name='student-delete'),
    path('chart1/', Chart1, name='chart1'),
]