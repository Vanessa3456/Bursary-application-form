from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
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
    status_filter= request.GET.get('status',None)
    if status_filter and status_filter != 'all':
        applications=applications.filter(application_status=status_filter)
        
    # get counts for each status
    pending_count=Rattansi.objects.filter(applications_status='pending').count()
    approved_count=Rattansi.objects.filter(applications_status='approved').count()
    rejected_count=Rattansi.objects.filter(applications_status='rejected').count()
    
    return render(request, 'admin_dashboard.html',{
        'applications':applications,
        'pending_count':pending_count,
        'approved_count':approved_count,
        'rejected_count':rejected_count,
        'status_filter':status_filter or 'all',       
    })
    
@login_required
def apply_for_bursary(request):
    # check if user  already has a pending application
    has_pending=Rattansi.objects.filter(
        student=request.user,
        application_status='pending'
    ).exists()
    
    if has_pending:
        messages.warning(request,"You already have a pending application. You cannot submit another one until the current application is process")
        return redirect('student_dashboard')
    
    if request.method == 'POST':
        form = RattansiBursaryApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application= form.save(commit=False)
            application.student=request.user
            application.save()
            messages.success(request, "Your bursary application has been submitted succefully.")
            return redirect('student_dashboard')
        else:
            form=RattansiBursaryApplicationForm()
            return render(request, 'apply_for_bursary.html',{'form':form})
        
@login_required
def application_detail(request, application_id):
    application=get_object_or_404(Rattansi,id=application_id)
    
    # ensure only the admin can view the application
    if application.student != request.user and not(request.user.is_admin or request.user.is_staff):
        messages.error(request, "You are not authorized to view this application")
        return redirect('student_dashboard')
    return redirect(request, 'application_details.html',{'application':application})

@login_required
@user_passes_test(is_admin)
def update_application_status(request, application_id):
    application= get_object_or_404(Rattansi, id=application_id)
    
    if request.method == 'POST':
        new_status=request.POST.get('application_status')
        amount_awarded= request.POST.get('amount_awarded',None)
        dean_comments=request.POST.get('dean_comments','')
        
        if new_status in [choice[0] for choice in Rattansi.STATUS_CHOICES]:
            application.application_status=new_status
            application.school_dean_comments=dean_comments
            
            if new_status == 'approved' and amount_awarded:
                application.amount_awarded=amount_awarded
            
                application.save()
                messages.success(request, f"Application status updated to {new_status}.")
            else:
                messages.error(request, "Invalid status provided")
            
        return redirect('application_detail',application_id=application_id)
    
@login_required
def download_attachment(request, application_id, file_type):
    application=get_object_or_404(Rattansi, id=application_id)
    
    # ensure only the owner or admin can download attachments
    if application.student != request.user and not (request.user.is_admin or request.user.is_staff):
        messages.error(request, "You are not authorized to download this file.")
        return redirect('student_dashboard')
    
    # determine which file to save
    if file_type == 'fee_statement' and application.fee_statement:
        file_path= application.fee_statement.path
    elif file_type == 'death_certificate' and application.death_certificate:
        file_path=application.death_certificate.path
    elif file_type == 'health_documents' and application.health_documents:
        file_path=application.health_documents.path
    elif file_type == 'other_documents' and application.other_documents:
        file_path=application.other_documents.path
    else:
        messages.error(request, "The requested file does not exist.")
        return redirect('application_detail')
    application_id=application_id
    
    # check if file exists and serve it
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response= HttpResponse(fh.read(), content_type='application/octet-stream')
            response['Content-Disposition']=f'attachment filename={os.path.basename(file_path)}'
            return response
    else:
        messages.error(request, "File not found.")
        return redirect('application_detail',application_id=application_id)
    
            
        
    
            
                
                
                
            
        
        
    
            
    
    
    
    

    
    

    
                

