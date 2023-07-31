from django.conf import settings
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.urls import reverse_lazy, reverse
from results.forms import PrintResultForm, ResultUploadForm
from django.contrib import messages
from results.models import UploadResult, Result
from results.filters import MyresultFilter
from students.models import StudentDetail
import os
from django_filters.views import FilterView
# For panigation
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

@login_required
def printresult(request):
    result = UploadResult.objects.all()
    context = {
        'result':result
    }
    
    return render(request, 'results/view_result.html', context)



@login_required
def printresultform(request):
    if request.method == 'POST':
        print_form = PrintResultForm(request.POST, request.FILES)
                        
        if print_form.is_valid():
             print_form.save()
             messages.success(request, f'Your upload is successful, enter another or refresh the page')
             
             return HttpResponseRedirect(reverse("results:print-resultform"))
             

        
    else:
        print_form = PrintResultForm()
    
        # file = PrintResult.objects.all()
        # 'print_form': print_form
   
    return render(request, 'results/upload_result.html', {'print_form': print_form})





@login_required
def uploadresult(request):
    if request.method == 'POST':
        upload_form = ResultUploadForm(request.POST)
                      
        if upload_form.is_valid():
             upload_form.save()
             messages.success(request, f'The Result has been uploaded successfully')
             return redirect('studentpage')
        
    else:
        upload_form = ResultUploadForm()
    context ={
        'upload_form' : upload_form
    }

    return render(request, 'results/result_entry_form1.html', context)

# FUNCTION FOR DOWNLOADING FILE
def download(request,path):
    file_path=os.path.join(settings.MEDIA_ROOT,path)
    if os.path.exists(file_path):
        with open(file_path, 'rb')as fh:
            response=HttpResponse(fh.read(),content_type="application/file")
            response['Content-Disposition']='inline;filename='+os.path.basename(file_path)
            return response

    raise Http404



@login_required
def view_self_result(request, **kwargs):
# this issue was solved by me.
    myresult = UploadResult.objects.filter(student_id=StudentDetail.objects.get(user_id=request.user))
    myresult_filter = MyresultFilter(request.GET, queryset=myresult) 
    myresult = myresult_filter.qs
    

     # PAGINATOR METHOD
    page = request.GET.get('page', 1)
    paginator = Paginator(myresult, 10)
    try:
        myresult = paginator.page(page)
    except PageNotAnInteger:
        myresult = paginator.page(1)
    except EmptyPage:
        myresult = paginator.page(paginator.num_pages)
   


    try:     
        myresult = UploadResult.objects.filter(student_id=StudentDetail.objects.get(user_id=request.user))
    
        context = {
            'myresult' : UploadResult.objects.filter(student_id=StudentDetail.objects.get(user_id=request.user)),
            'myresult':myresult,
            'myresult_filter' : myresult_filter,
            
        }    
    
        return render(request, 'results/view_self_result.html', context)

    except StudentDetail.DoesNotExist:
        return HttpResponse('<div style="text-align:center; padding-top:100px;"><h1 > Oops! You are not a student</h1>'
                                '<p>Please <a href="#">register</a> as a student</p>'
                                '</div>'
                                )
        

# FUNCTION FOR DOWNLOADING FILE
def download(request,path):
    file_path=os.path.join(settings.MEDIA_ROOT,path)
    if os.path.exists(file_path):
        with open(file_path, 'rb')as fh:
            response=HttpResponse(fh.read(),content_type="application/file")
            response['Content-Disposition']='inline;filename='+os.path.basename(file_path)
            return response

    raise Http404


@login_required
def view_self_reportsheet(request, **kwargs):
# this issue was solved by me.
    try:     
        myreportsheet = Result.objects.filter(student_id=StudentDetail.objects.get(user_id=request.user)).order_by("-id")
    
        context = {
            'myreportsheet':myreportsheet
            
        }    
    
        return render(request, 'results/my_reportsheet.html', context)

    except StudentDetail.DoesNotExist:
        return HttpResponse('<div style="text-align:center; padding-top:100px;"><h1 > Oops! You are not a student</h1>'
                                '<p>Please <a href="#">register</a> as a student</p>'
                                '</div>'
                                )
      
        