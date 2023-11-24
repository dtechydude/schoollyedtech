from django.conf import settings
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.urls import reverse_lazy, reverse
from results.forms import PrintResultForm, ResultUploadForm, ResultCreateForm, ResultUpdateForm
from django.contrib import messages
from results.models import UploadResult, MarkedSheet, ResultSheet
from results.filters import MyresultFilter, MyResultSheetFilter, ResultSheetFilter
from students.models import StudentDetail
import os
from django_filters.views import FilterView
# For panigation
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import(TemplateView, DetailView,
                                ListView, FormView, CreateView, 
                                UpdateView, DeleteView)
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.http import FileResponse
import csv

# Create your views here.

@login_required
def printresult(request):
    result = ResultSheet.objects.all()
    resultsheet_filter = ResultSheetFilter(request.GET, queryset=result) 
    result = resultsheet_filter.qs
    

     # PAGINATOR METHOD
    page = request.GET.get('page', 1)
    paginator = Paginator(result, 30)
    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)

    try:     
        # result = ResultSheet.objects.filter(student_id=StudentDetail.objects.get(user_id=request.user))
    
        context = {
            # 'result' : resultsheet_filter.objects.filter(student_id=StudentDetail.objects.get(student_id=request.user)),
            'result':result,
            'resultsheet_filter' : resultsheet_filter,
            
        }

        return render(request, 'results/view_result.html', context)

    except StudentDetail.DoesNotExist:
        return HttpResponse('<div style="text-align:center; padding-top:100px;"><h1 > Oops! You are not a student</h1>'
                            '<p>Please <a href="#">register</a> as a student</p>'
                            '</div>'
                            )
        



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
def download(request, path):
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
      
        
@login_required
def resultsheet(request):
    resultsheet = ResultSheet.objects.all()
    context = {
        'resultsheet':resultsheet
    }
    
    return render(request, 'results/result_sheet.html', context)


@login_required
def result_create_form(request):
    if request.method == 'POST':       
        result_create_form = ResultCreateForm(request.POST)

        if result_create_form.is_valid():         
            result_create_form.save()
            messages.success(request, f'The Result has been entered successfully, add another one')
            return redirect('results:result-create')
    else:
        result_create_form = ResultCreateForm()

    context ={
        'result_create_form' : result_create_form
    }
    return render(request, 'results/result_create_form.html', context)



class ResultDetailView(LoginRequiredMixin, DetailView):
    model = ResultSheet
    context_object_name = 'my_resultsheet'
    template_name = 'results/result_sheet.html'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        new_str = self.kwargs.get('pk') or self.request.GET.get('pk') or None

        queryset = queryset.filter(pk=new_str)
        obj = queryset.get()
        return obj

    def result_calculation(request):
       
        total_score = ResultSheet.objects.annotate(total_score= F('score_1ca') + F('score_1exam'))


@login_required
def view_self_result(request):
    # mypayment = PaymentDetail.objects.filter(student=StudentDetail.objects.get(user=request.user))
    # myresultsheet = ResultSheet.objects.filter(student_id=User.objects.get(username=request.user))
    myresultsheet = ResultSheet.objects.filter(student_detail=StudentDetail.objects.get(user=request.user))
    myresultsheet_filter = MyResultSheetFilter(request.GET, queryset=myresultsheet)
    myresultsheet = myresultsheet_filter.qs

    page = request.GET.get('page', 1)
    paginator = Paginator(myresultsheet, 20)
    try:
        myresultsheet = paginator.page(page)
    except PageNotAnInteger:
        myresultsheet = paginator.page(1)
    except EmptyPage:
        myresultsheet = paginator.page(paginator.num_pages)
    context = {
        # 'mypayment' : PaymentDetail.objects.filter(student=StudentDetail.objects.get(user=request.user)).order_by("-payment_date"),
        'myresultsheet' : ResultSheet.objects.filter(student_id=User.objects.get(username=request.user)).order_by("exam_date"),
        'myresultsheet':myresultsheet,
        'myresultsheet_filter' : myresultsheet_filter,
    }

    return render(request, 'results/result_self_list.html', context)


#Result Detail
class ResultListView(LoginRequiredMixin, ListView):
    context_object_name = 'result'
    model = ResultSheet
    queryset = ResultSheet.objects.all()
    template_name = 'results/view_result.html'
    paginate_by = 2
    # filterset_class = StudentFilter


class ResultUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ResultUpdateForm
    template_name = 'results/result_update_form.html'
    queryset = ResultSheet.objects.all()
    success_url = '/results/result-list/'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(ResultSheet, id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def get_success_url(self):
        return  ('/results/result-list/')



def results_csv(request):
    response = HttpResponse(content_type ='text/csv')
    response['Content-Disposition'] = 'attachment; filename=results.csv'
    
# Create a csv writer
    writer = csv.writer(response)

    results = ResultSheet.objects.all()
    
    # Add column headings to the csv files
    writer.writerow(['USERNAME', 'FIRST NAME', 'MIDDLE NAME', 'LAST NAME', 'CURRENT CLASS', 'EXAM', 'SESSION', 'TERM', 'SUBJECT 1', 'C.A', 'EXAM', 'TOTAL', 'SUBJECT 2', 'C.A', 'EXAM', 'TOTAL',
                        'SUBJECT 3', 'C.A', 'EXAM', 'TOTAL', 'SUBJECT 4', 'C.A', 'EXAM', 'TOTAL', 'SUBJECT 5', 'C.A', 'EXAM', 'TOTAL', 'SUBJECT 6', 'C.A', 'EXAM', 'TOTAL', 'SUBJECT 7', 'C.A', 'EXAM', 'TOTAL',
                        'SUBJECT 8', 'C.A', 'EXAM', 'TOTAL', 'SUBJECT 9', 'C.A', 'EXAM', 'TOTAL', 'SUBJECT 10', 'C.A', 'EXAM', 'TOTAL', 'SUBJECT 11', 'C.A', 'EXAM', 'TOTAL',
                        'SUBJECT 12', 'C.A', 'EXAM', 'TOTAL', 'SUBJECT 13', 'C.A', 'EXAM', 'TOTAL', 'SUBJECT 14', 'C.A', 'EXAM', 'TOTAL', 'SUBJECT 15', 'C.A', 'EXAM', 'TOTAL', 'SUBJECT 16', 'SUBJECT 17', 'SUBJECT 18', 'SUBJECT 19', 'SUBJECT 20',  'C.A', 'EXAM', 'TOTAL', 'OVERALL %' ])


    # Loop thru and output
    for result in results:
        writer.writerow([result.student_id, result.student_detail.first_name, result.student_detail.middle_name, result.student_detail.last_name, result.standard, result.exam, result.session, result.term,
                        result.subject_1, result.score_1ca, result.score_1exam, result.total_score_1, result.subject_2, result.score_2ca, result.score_2exam, result.total_score_2, result.subject_3, result.score_3ca, result.score_3exam, result.total_score_3, result.subject_4, result.score_4ca, result.score_4exam, result.total_score_4,
                        result.subject_5, result.score_5ca, result.score_5exam, result.total_score_5, result.subject_6, result.score_6ca, result.score_6exam, result.total_score_6, result.subject_7, result.score_7ca, result.score_7exam, result.total_score_7, result.subject_8, result.score_8ca, result.score_8exam, result.total_score_8,
                        result.subject_9, result.score_9ca, result.score_9exam, result.total_score_9, result.subject_10, result.score_10ca, result.score_10exam, result.total_score_10, result.subject_11, result.score_11ca, result.score_11exam, result.total_score_11, result.subject_12, result.score_12ca, result.score_12exam, result.total_score_12,
                        result.subject_13, result.score_13ca, result.score_13exam, result.total_score_13, result.subject_14, result.score_14ca, result.score_14exam, result.total_score_14, result.subject_15, result.score_15ca, result.score_15exam, result.total_score_15, result.subject_16, result.score_16ca, result.score_16exam, result.total_score_16,
                        result.subject_17, result.score_17ca, result.score_17exam, result.total_score_17, result.subject_18, result.score_18ca, result.score_18exam, result.total_score_18, result.subject_19, result.score_19ca, result.score_19exam, result.total_score_19, result.subject_20, result.score_20ca, result.score_20exam, result.total_score_20,
                        result.overall_percentage])
        
    return response