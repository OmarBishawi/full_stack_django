from django.shortcuts import render,redirect
from django.contrib import messages
from .models import User
from datetime import datetime


def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        birthday = request.POST.get('birthday')

        errors=[]
        if len(first_name) <2:
            errors.append("First name should be at least 2 characters long.")
        if len(last_name) < 2:
            errors.append("Last name should be at least 2 characters long.")
        if User.objects.filter(email=email).exists():
            errors.append("Email already exists.")
        if len(password1) < 8:
            errors.append("Password should be at least 8 characters long.")
        if password1 != password2:
            errors.append("passwords do not match.")
        if birthday:
            try:
                birthday_date = datetime.strptime(birthday, "%Y-%m-%d").date()
                if birthday_date > datetime.now().date():
                    errors.append("Birthday cannot be in the future.")
            except ValueError:
                errors.append("Invalid date format for birthday.")

        if errors:
            for error in errors:
                messages.error(request,error)
            return redirect('registration')
        #if no errors create user
        
        #create user
        user = User(first_name = first_name ,last_name = last_name ,email = email , password = password1, birthday = birthday)
        user.save()
        messages.success(request, "Successfully registered! Please log in.")     #for feed back
        return redirect ('login')
    return render(request , 'register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try :
            user = User.objects.get(email = email , password = password)
            request.session['user_id']= user.id
            return redirect ('success')
        except User.DoesNotExist:
            messages.error(request, "invalid email or password")
            return redirect ('login')
    return render(request, 'login.html')

def success(request):
    if 'user_id' not in request.session :
        return redirect('login')
    user = User.objects.get( id = request.session ['user_id'])
    return render(request ,'success.html', {'user': user})

def logout_view(request):
    if 'user_id' not in request.session :
        del request.session['user_id']
    return redirect ('login')





# Create your views here.
