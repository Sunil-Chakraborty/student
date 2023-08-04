from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView
from student_app.workings import  ExcelView
from chartapp.views import ChartView
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from account.views import(    
    account_register,
    account_login,
    logout_view,
    dashboard_view,
    
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls', namespace='account')),
    
    path('student/', include('student_app.urls', namespace='student')),
    path('product/', include('product.urls', namespace='product')),
    path('xlview', ExcelView, name='xlview'),
    path('chart/', ChartView, name='chart'),
    path('', account_register, name="register"),
    path('login/', account_login, name="login"),
    path('logout/', logout_view, name="logout"),    
    path('dashboard/', dashboard_view, name="dashboard"),
   
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
