import os
from django.http import HttpResponse
from django import template
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from .forms import CreateComplaintForm, CreateFeedbackForm
from django.contrib.auth.decorators import login_required
from services.models import (Complaint,Feedback,Department)
from accounts.models import MyUser

register = template.Library()

@login_required
def home(request,type):
    complaints = ''
    if type=='student':
        complaints = Complaint.objects.filter(sender = request.user)
    elif type == 'chair':
        dep = Department.objects.get(chairperson=request.user)
        complaints = Complaint.objects.filter(department = dep)
    departments = Department.objects.all()
    
    solved_tickets = complaints.filter(status='Solved')
    pending_tickets = complaints.filter(status='Pending')
    
    f = CreateComplaintForm()
    
    if request.method == 'POST':
        if 'solved' in request.POST:
            id = request.POST.get('id')
            complaint = Complaint.objects.get(pk=id)
            complaint.status = 'Solved'
            complaint.save()
            return redirect(f'/home/{type}/')
            #success message
            
        if 'transfer' in request.POST:
            id = request.POST.get('id')
            department = request.POST.get('department')
            complaint = Complaint.objects.get(pk=id)
            depart = Department.objects.get(pk=department)
            print(department)
            complaint.department = depart
            complaint.save()
            return redirect(f'/home/{type}/')
        
        if 'create-comp' in request.POST:
            department = request.POST.get('department')
            problem = request.POST.get('problemDetail')
            file = request.FILES.get('myfile')
            depart = Department.objects.get(pk=department)
            if file:
                complaint = Complaint(sender = request.user, message=problem, file=file, department=depart)
            else:
                complaint = Complaint(sender = request.user, message=problem, department=depart)
            complaint.save()
            return redirect(f'/home/{type}/')
            #success message
    
    context = {
        'complaints':complaints,
        'solved':solved_tickets,
        'pending':pending_tickets,
        'departments' : departments,
        'type':type,
    }
    
    return render(request, 'app/index.html', context)

@register.filter(name='get_file_type')
def get_file_type(filename):
    ext = os.path.splitext(filename)[-1].lower()
    if ext in {".jpg", ".jpeg", ".png"}:
        return "Image"
    elif ext in {".docx", ".doc"}:
        return "Word Document"
    elif ext == ".pdf":
        return "PDF"
    else:
        return "Unknown"
register.filter(name='get_file_type')

@login_required
def viewComp(request, pk):
    complaint = Complaint.objects.get(pk=pk)
    
    filename = ""
    if complaint.file:
        filename = filename = os.path.basename(complaint.file.name) 
    file_type = get_file_type(filename)
    context = {
        'complaint': complaint,
        'file_type' : file_type,
    }
    return render(request, 'app/complaint.html', context)

@login_required
def viewFeebacks(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    feedbacks = Feedback.objects.filter(complaint=complaint)
    
    for feedback in feedbacks:
        if feedback.sender != request.user:
            feedback.read = True
            feedback.save()
    
    if request.method == 'POST':
        form = CreateFeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.complaint = complaint
            if not isinstance(request.user, MyUser):
                return HttpResponse("Unauthorized", status=401)
            form.instance.sender = request.user
            form.save()
            return redirect(f'/feedbacks/{pk}/')
    
    context = {
        'complaint': complaint,
        'feedbacks': feedbacks,
    }
    return render(request, 'app/feedbacks.html', context)

# Create your views here.
