from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count
from students.models import StudentDetail
from staff.models import StaffProfile
from notification.models import SchoolCalendar
from django.views.generic import  ListView
from .forms import ClassRegisterForm, ClassgroupRegisterForm, SessionRegisterForm, ExamRegisterForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

@login_required
def portal_home(request):
    users_num = User.objects.count()
    student_num = StudentDetail.objects.count()
    num_inclass = StudentDetail.objects.filter(current_class__name='Jss1').count()
    num_student_inclass = StudentDetail.objects.filter().count()
    graduated = StudentDetail.objects.filter(student_status='graduated').count()
    dropped = StudentDetail.objects.filter(student_status='dropped').count()
    expelled = StudentDetail.objects.filter(student_status='expelled').count()
    suspended = StudentDetail.objects.filter(student_status='suspended').count()
    active = StudentDetail.objects.filter(student_status='active').count()
    staff_num = StaffProfile.objects.count()
    students = StudentDetail.objects.filter().order_by('current_class').values('current_class__name').annotate(count=Count('current_class__name'))
    
    # Build a paginator with function based view
    queryset = SchoolCalendar.objects.all().order_by("-id")
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 4)
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)
    
    context = {
        'student_num': student_num,
        'students' : students,
        'users_num': users_num,
        'num_inclass': num_inclass,
        'staff_num': staff_num,
        'graduated': graduated,
        'dropped': dropped,
        'expelled': expelled,
        'suspended': suspended,
        'active': active,
        'queryset': queryset,
        'events':events,
    }
    return render(request, 'portal/portal-home.html', context)


@login_required
def register_new_standard(request):
    if request.method == 'POST':
        
        new_class_form = ClassRegisterForm(request.POST)
        if new_class_form.is_valid():
           
            new_class_form.save()
            messages.success(request, f'New Class Registered successfully, Register another or go to class list')
            return redirect('portal:register-class')
    else:
      
        new_class_form = ClassRegisterForm

    context = {
        
        'new_class_form': new_class_form,
    }

    return render(request, 'portal/register_new_standard.html', context)

# Section/Classgroup Registration
@login_required
def register_new_classgroup(request):
    if request.method == 'POST':
        
        new_class_group = ClassgroupRegisterForm(request.POST)
        if new_class_group.is_valid():
           
            new_class_group.save()
            messages.success(request, f'New Class Group Registered successfully, Register another or go to class list')
            return redirect('portal:register-classgroup')
    else:
      
        new_class_group = ClassgroupRegisterForm

    context = {
        
        'new_class_group': new_class_group,
    }

    return render(request, 'portal/register_new_classgroup.html', context)


@login_required
def register_new_session(request):
    if request.method == 'POST':
        
        new_session = SessionRegisterForm(request.POST)
        if new_session.is_valid():
           
            new_session.save()
            messages.success(request, f'New Session Registered successfully, Register another or go to class list')
            return redirect('portal:register-session')
    else:
      
        new_session = SessionRegisterForm

    context = {
        
        'new_session': new_session,
    }

    return render(request, 'portal/register_new_session.html', context)


@login_required
def register_exam(request):
    if request.method == 'POST':
        
        new_exam = ExamRegisterForm(request.POST)
        if new_exam.is_valid():
           
            new_exam.save()
            messages.success(request, f'New Exam Registered successfully, Register another or go to class list')
            return redirect('portal:register-exam')
    else:
      
        new_exam = ExamRegisterForm

    context = {
        
        'new_exam': new_exam,
    }

    return render(request, 'portal/register_exam.html', context)


    