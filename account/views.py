from django.shortcuts import render, get_object_or_404, redirect,reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from .email_backend import EmailBackend
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm
#from django.contrib.auth.views import LoginView
from . models import Account,Department
from django.contrib.auth.models import User


def account_register(request):
    userForm = RegistrationForm(request.POST or None)
    
    context = {
        'form1': userForm,
        'registration_form':userForm
    }
    if request.method == 'POST':
        if userForm.is_valid():            
            user = userForm.save(commit=False)
            user.faculty = Department.objects.filter(name=user.Department).values_list('faculty', flat=True).first()
            user.dept_name = Department.objects.filter(name=user.Department).values_list('name', flat=True).first()
            user.save()
            messages.success(request, "Account created. You can login now!")
            #return redirect(reverse('login'))
            return redirect(request.path)
        else:            
            messages.error(request, "Provided data failed validation")
            # return account_login(request)
    
    return render(request, "login.html", context)


def account_login(request):
   
    context = {}
    if request.method == 'POST':
        user = EmailBackend.authenticate(request, username=request.POST.get(
            'email'), password=request.POST.get('password'))
        if user != None:
            message = "Your request was successful!"
            #return HttpResponseRedirect(reverse('home') + "?message=" + message)
            #print(user.id)
            user_id = user.id
            request.session['user_id'] = user_id
            print('l-47',user_id)
            return redirect('dashboard')
            
            #return redirect(request.path)
            #login(request, user)
        else:
            
            messages.error(request, "Invalid details")
            return redirect("/")

    return render(request, "login.html", context)

def logout_view(request):
    logout(request)
    return redirect("/")

def dashboard_view(request):

    context={}
    
    return render(request, "dashboard.html", context)
