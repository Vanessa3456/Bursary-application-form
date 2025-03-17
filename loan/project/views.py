from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_list_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import StudentRegistrationForm, RattansiBursaryApplicationForm
from .models import Rattansi
from django.utils import timezone
from django.http import HttpResponse
from django.conf import settings
import os

def home(request):
    # get the current academic year(assuming September to April)
    current_date=timezone.now()
    if current_date.month >=9:
            # The academic year starts in the current year and ends in the next year
        academic_year= f"{current_date.year}/{current_date.year+1}" # the format for the academic year is "YYYY/YYYY+1" eg "2024/2025"
    else:
            # The academic year started in the previous year and ends in the current year
        academic_year=f"{current_date.year-1}/{current_date.year}"
        
    # check if application period is active
    application_active=True #will be controlled in the admin panel
    
    return render(request, 'home.html',{
        'academic_year':academic_year,
        'application_active':application_active
    })

def register(request):
    if request.method=='POST':
        form=StudentRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            messages.success(request,"Registration succesful. You can now apply for the bursary.")
            return redirect('student_dashboard')
    else:
        form = StudentRegistrationForm()
        return render(request,'register.html',{'form':form})
    
def login_view(request):
    if  request.method == 'POST':
        form=AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username= form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                if user.is_admin or user.is_staff:
                    return redirect('admin_dashboard')
                else:
                    return redirect('student_dashboard')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    else:
        form= AuthenticationForm()
    return render(request, 'login.html',{
        'form':form
    })

def logout_view(request):
    logout(request)
    messages.success(request, "You have succesfully logged out.")
    return redirect('home')

def is_admin(user):
    return user.is_admin or user.is_staff

@login_required
def student_dashboard(request):
    # get student's application
    applications=Rattansi.objects.filter(student=render.user).order_by('-created_at')
    
    # check if the application period is active
    application_active=True
    
    # get the current academic year
    current_date= timezone.now()
    if current_date.month >= 9 :
        academic_year=f"{current_date.year}/{current_date.year+1}"
    else:
        academic_year=f"{current_date.year-1}/{current_date.year}"
    
    return render(request, 'student_dashboard.html',{
        'applications':applications,
        'application_active':application_active,
        'academic_year':academic_year
    })
    
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # get all applications
    applications=Rattansi.objects.all().order_by('-created_at')
    
    # filter applications based on status provided
    

    
                

