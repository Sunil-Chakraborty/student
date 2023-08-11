from django.shortcuts import render, get_object_or_404, redirect,reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from .email_backend import EmailBackend
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from account.forms import RegistrationForm, MessageForm
#from django.contrib.auth.views import LoginView
from . models import Account,Department
#from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Message
from django.utils.html import strip_tags


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
            print('l-49',user_id)
            recd_msg = Message.objects.filter(receiver=user_id)
            if recd_msg :
                return redirect('account:inbox')
            else:    
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


@login_required
def send_message(request, receiver_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        receiver = User.objects.get(id=receiver_id)
        message = Message.objects.create(sender=request.user, receiver=receiver, content=content)
        return redirect('inbox')  # Replace 'inbox' with the name of your view displaying received messages
    else:
        receiver = User.objects.get(id=receiver_id)
        return render(request, 'account/send_message.html', {'receiver': receiver})


def inbox(request,*args, **kwargs):    
    user_id = request.session['user_id']
    account = Account.objects.get(pk=user_id)
    
    print("l-90 ",user_id)
    received_messages = Message.objects.filter(receiver=user_id,read=False)
    sending_message = Message.objects.filter(sender=user_id) 
    
    if received_messages or sending_message or user_id == 1 : 
        return render(request, 'account/inbox.html', {'messages': received_messages,'sending_message': sending_message,'account':account})
    else:
        return redirect('dashboard')
        
      
def create_message(request):
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        
        receiver = request.POST.get('receiver')
        account = Account.objects.get(pk=receiver)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.receiver_name = account.username
            user.email = account.email
            user.save()
            return redirect('account:inbox')
        
        
    form = MessageForm()     
    return render(request, 'account/create_message.html', {'form': form})

def edit_message(request, message_id):
    message = Message.objects.get(pk=message_id)
    content_text=message.content
    user_id = request.session['user_id']
    account = Account.objects.get(pk=user_id)
    hide_sender = False
    hide_receiver = False
    
    if not account.is_superuser: 
        hide_sender = True  # Set this to True or False based on your condition
        hide_receiver = True  # Set this to True or False based on your condition
        
        
    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        receiver = request.POST.get('receiver')        
        account = Account.objects.get(pk=receiver)
        
        if form.is_valid():
            user = form.save(commit=False)
            
            user.receiver_name = account.username
           
            if hide_sender and hide_receiver:
                user.read = True
                
                print('l-145',user.content)
            else:
                user.timestamp = user.modified_date
                user.read = False
            user.email = account.email
            user.save()
            
            return redirect('account:inbox')
    else:
        form = MessageForm(instance=message)
    return render(request, 'account/edit_message.html', {'form': form, 'message': message,'hide_sender': hide_sender, 'hide_receiver': hide_receiver,'content_text':content_text})


def view_message(request,message_id):     
    
    message = get_object_or_404(Message, pk=message_id)
    
    if not message.read:        
        message.read = True       
        message.save()
       
    return redirect('dashboard')
    

def delete_message(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    message_subject = message.content  # Save the subject for displaying in the message

    message.delete()

    # Redirect to inbox after deletion
    return redirect('account:inbox')
