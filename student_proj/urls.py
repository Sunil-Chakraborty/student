from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView
from student_app.views import BootstrapFilterView
from student_app.workings import  ExcelView
from chartapp.views import ChartView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', BootstrapFilterView, name='bootstrap'),
    path('xlview', ExcelView, name='xlview'),
    path('chart/', ChartView, name='chart'),

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
