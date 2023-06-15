from django.contrib import admin
from .models import Student,Fin_Year,Courses,Faculty,Criteria


# Register your models here.

class StudentAdmin(admin.ModelAdmin):
	list_display = (
     'year','course_name','faculty','courses','intake','strength'
     )
 
 
admin.site.register(Student,StudentAdmin)

admin.site.register(Fin_Year)
admin.site.register(Courses)
admin.site.register(Faculty)
admin.site.register(Criteria)
