from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.db.models import F, Sum, Q
from payment.forms import PaymentForm, PaymentChartForm, PaymentCatForm,PaymentCreateForm, BankRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import os
from payment.models import PaymentDetail, PaymentChart, PaymentCategory, BankDetail
from students.models import StudentDetail
from django.http import HttpResponse
from django.http import FileResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import(ListView, FormView, CreateView, UpdateView, DeleteView, DetailView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# For Filter
from .filters import PaymentFilter, MyPaymentFilter, PaymentChartFilter, PaymentReportFilter, PaymentSummaryFilter
from django_filters.views import FilterView
# For panigation
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# for csv
import csv


# Create your views here.
@login_required
def payment_form(request):
    if request.method == 'POST':       
        payment_form = PaymentForm(request.POST)

        if payment_form.is_valid():         
            payment_form.save()
            messages.success(request, f'The Payment has been entered successfully')
            return redirect('payment:payment_form')
    else:
        payment_form = PaymentForm()

    context ={
        'payment_form' : payment_form
    }
    return render(request, 'payment/make_payment.html', context)

class PaymentCreateView(LoginRequiredMixin, CreateView):
    template_name = 'payment/student_payment_form.html'
    form_class = PaymentCreateForm
    
    success_url = reverse_lazy('payment:my_payments')

    def form_valid(self, form):
        print('form_valid called')
        object = form.save(commit=False)
        object.payee = self.request.user
        object.save()
        return super(PaymentCreateView, self).form_valid(form)



@login_required
def payment_cat_form(request):
    if request.method == 'POST':
        payment_cat_form = PaymentCatForm(request.POST)
        # p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if payment_cat_form.is_valid():
            payment_cat_form.save()

            messages.success(request, f'The Payment Category has been entered successfully')
            return redirect('payment:payment-category')
    else:
        payment_cat_form = PaymentCatForm()

    context ={
        'payment_cat_form' : payment_cat_form
    }
    return render(request, 'payment/payment_cat_form.html', context)


@login_required
def payment_chart_form(request):
    if request.method == 'POST':
        payment_chart_form = PaymentChartForm(request.POST)
        # p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if payment_chart_form.is_valid():
            payment_chart_form.save()

            messages.success(request, f'The Payment has been entered successfully')
            return redirect('payment:payment_chart')
    else:
        payment_chart_form = PaymentChartForm()

    context ={
        'payment_chart_form' : payment_chart_form
    }
    return render(request, 'payment/payment_chart_form.html', context)




@login_required
def paymentlist(request):
    paymentlist = PaymentDetail.objects.all()
    paymentlist_filter = PaymentFilter(request.GET, queryset=paymentlist)
    balance_pay = PaymentDetail.objects.annotate(balance_pay= F('amount_paid') - F('payment_name__amount_due'))
  

    paymentlist = paymentlist_filter.qs

    page = request.GET.get('page', 1)
    paginator = Paginator(paymentlist, 40)
    try:
        paymentlist = paginator.page(page)
    except PageNotAnInteger:
        paymentlist = paginator.page(1)
    except EmptyPage:
        paymentlist = paginator.page(paginator.num_pages)


    context = {
        'paymentlist': PaymentDetail.objects.all(),
        'paymentlist_filter': paymentlist_filter,
        'paymentlist' : paymentlist,
        'balance_pay': balance_pay,
        'balance_pay' : PaymentDetail.objects.annotate(balance_pay= F('amount_paid') - F('payment_name__amount_due'))
         

    }
    return render (request, 'payment/all_payments.html', context )

    # return render(request, 'payment/schoolly_test_table.html',)


@login_required
def view_self_payments(request):
    # mypayment = PaymentDetail.objects.filter(student=StudentDetail.objects.get(user=request.user))
    mypayment = PaymentDetail.objects.filter(payee=User.objects.get(username=request.user))
    mypayment_filter = MyPaymentFilter(request.GET, queryset=mypayment)
    mypayment = mypayment_filter.qs

    page = request.GET.get('page', 1)
    paginator = Paginator(mypayment, 40)
    try:
        mypayment = paginator.page(page)
    except PageNotAnInteger:
        mypayment = paginator.page(1)
    except EmptyPage:
        mypayment = paginator.page(paginator.num_pages)
    context = {
        # 'mypayment' : PaymentDetail.objects.filter(student=StudentDetail.objects.get(user=request.user)).order_by("-payment_date"),
        'mypayment' : PaymentDetail.objects.filter(payee=User.objects.get(username=request.user)).order_by("payment_date"),
        'mypayment':mypayment,
        'mypayment_filter' : mypayment_filter,
    }

    return render(request, 'payment/view_self_payment.html', context)


    


@login_required
def payment_chart_list(request):
    payment_chart_list = PaymentChart.objects.all()
    payment_chart_filter = PaymentChartFilter(request.GET, queryset=payment_chart_list)
    payment_chart_list = payment_chart_filter.qs
   

    page = request.GET.get('page', 1)
    paginator = Paginator(payment_chart_list, 40)
    try:
        payment_chart_list = paginator.page(page)
    except PageNotAnInteger:
        paymentChart = paginator.page(1)
    except EmptyPage:
        payment_chart_list = paginator.page(paginator.num_pages)


    context = {
        'payment_chart_list': PaymentDetail.objects.all(),
        'payment_chart_filter' : payment_chart_filter,
        'payment_chart_list' : payment_chart_list

    }
    return render (request, 'payment/payment_chart.html', context )



# FUNCTION FOR DOWNLOADING FILE
def download(request,path):
    file_path=os.path.join(settings.MEDIA_ROOT,path)
    if os.path.exists(file_path):
        with open(file_path, 'rb')as fh:
            response=HttpResponse(fh.read(),content_type="application/file")
            response['Content-Disposition']='inline;filename='+os.path.basename(file_path)
            return response

    raise Http404


#  Function for pdf and csv

# Generate a PDF staff list
def allpayment_pdf(request):
    # create Bytestream buffer
    buf = io.BytesIO()
    #create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 12)
    # Add some lines of text
    # lines = [
    #     "This is line 1",
    #     "This is line 2",
    #     "This is line31",
    #     "This is line 4",
    # ]
    # Designate the model
    payment = PaymentDetail.objects.all()

    # Create a blank list

    lines = [" PAYMENT DETAIL REPORT"]

    for payments in payment:
        lines.append(""),
        lines.append("Username: " + payments.payee.username),
        lines.append("Amount: " + str(payments.amount_paid)),
        lines.append("Date: " + str(payments.payment_date)),
        lines.append("Method:" + payments.payment_method),

        lines.append("------->----------->----------->"),


    # loop
    for line in lines:
        textob.textLine(line)
    #fininsh up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    # Return something
    return FileResponse(buf, as_attachment=False, filename='payment.pdf')


# Generate a CSV staff list
def allpayment_csv(request):
    response = HttpResponse(content_type ='text/csv')
    response['Content-Disposition'] = 'attachment; filename=payment.csv'

# Create a csv writer
    writer = csv.writer(response)

    payment = PaymentDetail.objects.all()

    # Add column headings to the csv files
    writer.writerow(['STUDENT ID', 'SURNAME ', 'FIRSTNAME', 'CURRENT CLASS', 'FEE DUE', 'AMOUNT PAID', 'BALANCE', 'PURPOSE', 'PAYMENT DATE', 'METHOD', 'DEPOSITOR', 'BANK', 'DESCRIPTION', 'IS_CONFIRMED', 'SESSION', 'TERM'])


    # Loop thru and output
    for payments in payment:
        writer.writerow([payments.payee.username, payments.student_detail.last_name, payments.student_detail.first_name, payments.student_detail.current_class, payments.payment_name.amount_due, payments.amount_paid, payments.payment_name.amount_due - payments.amount_paid, 
        payments.payment_name, payments.payment_date, payments.payment_method, payments.depositor, payments.bank_name, payments.description, payments.confirmed, payments.payment_name.session, payments.payment_name.term])

    return response


def payment_chart_pdf(request):
    # create Bytestream buffer
    buf = io.BytesIO()
    #create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 12)
    # Add some lines of text

    # Designate the model
    payment_chart = PaymentChart.objects.all()

    # Create a blank list

    lines = [" PAYMENT CHART "]

    for payment in payment_chart:
        lines.append(""),
        lines.append("PAYMENT NAME: " + payment.name),
        lines.append("CATEGORY: " + str(payment.payment_cat)),
        lines.append("SESSION: " + str(payment.session)),
        lines.append("TERM:" + payment.term),
        lines.append("AMOUNT:" + payment.amount_due),

        lines.append("------->----------->----------->"),


    # loop
    for line in lines:
        textob.textLine(line)
    #fininsh up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    # Return something
    return FileResponse(buf, as_attachment=False, filename='payment_chart.pdf')


# Generate a CSV staff list
def payment_chart_csv(request):
    response = HttpResponse(content_type ='text/csv')
    response['Content-Disposition'] = 'attachment; filename=payment_chart.csv'

# Create a csv writer
    writer = csv.writer(response)

    payment_chart = PaymentChart.objects.all()

    # Add column headings to the csv files
    writer.writerow(['PAYMENT NAME ', 'CATEGORY', 'SESSION', 'TERM', 'AMOUNT DUE',])


    # Loop thru and output
    for payment in payment_chart:
        writer.writerow([payment.name, payment.payment_cat, payment.session,
        payment.term, payment.amount_due,])

    return response

#This code generates the receipt
class PaymentDetailView(LoginRequiredMixin, DetailView):
    model = PaymentDetail
    context_object_name = 'my_receipt'
    template_name = 'payment/receipt.html'
    

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        new_str = self.kwargs.get('pk') or self.request.GET.get('pk') or None

        queryset = queryset.filter(pk=new_str)
        obj = queryset.get()
        return obj


@login_required
def payment_report(request):
    paymentlist = PaymentDetail.objects.all()
    total_pay = PaymentDetail.objects.values('student_detail__student_username', 'student_detail__first_name', 'payment_name__amount_due', 'payment_name__name').annotate(total_payment=Sum('amount_paid')).order_by('student_detail')
    paymentreport_filter = PaymentReportFilter(request.GET, queryset=paymentlist)
    balance_pay = PaymentDetail.objects.annotate(balance_pay= F('amount_paid') - F('payment_name__amount_due'))

  

    paymentlist = paymentreport_filter.qs

    page = request.GET.get('page', 1)
    paginator = Paginator(paymentlist, 40)
    try:
        paymentlist = paginator.page(page)
    except PageNotAnInteger:
        paymentlist = paginator.page(1)
    except EmptyPage:
        paymentlist = paginator.page(paginator.num_pages)


    context = {
        'paymentlist': PaymentDetail.objects.all(),
        'paymentreport_filter': paymentreport_filter,
        'paymentlist' : paymentlist,
        'balance_pay': balance_pay,
        'total_pay': total_pay,
        'balance_pay' : PaymentDetail.objects.annotate(balance_pay= F('amount_paid') - F('payment_name__amount_due')),
   
    }
   
    return render(request, 'payment/payment_report_table.html', context )
    
    
@login_required
def summary_payment_report(request):
    allpayments = PaymentDetail.objects.all()
    total_pay = PaymentDetail.objects.values('student_detail__student_username', 'student_detail__first_name', 'student_detail__last_name',
                                            'payment_name__amount_due', 'payment_name__name', 'payment_name__session__name', 'student_detail__current_class__name',
                                            'payment_name__term', 'discount').annotate(total_payment=Sum('amount_paid')).order_by('student_detail')
    
    allpayments_filter = PaymentSummaryFilter(request.GET, queryset=total_pay)
    
    allpayments = allpayments_filter.qs

    page = request.GET.get('page', 1)

    paginator = Paginator(total_pay, 40)
    try:
        total_pay = paginator.page(page)
    except PageNotAnInteger:
        total_pay = paginator.page(1)
    except EmptyPage:
        total_pay = paginator.page(paginator.num_pages)


    context = {

        'total_pay': total_pay,
        'allpayments':allpayments,
        'allpayments': PaymentDetail.objects.all(),
        'allpayments_filter' : allpayments_filter,
     

   
    }
   
    return render(request, 'payment/summary_report.html', context )



class PaymentCategoryListView(LoginRequiredMixin, ListView):
    context_object_name = 'categorylist'
    model = PaymentCategory
    queryset = PaymentCategory.objects.all()
    template_name = 'payment/payment_cat_list.html'
    paginate_by = 30

class BankListView(LoginRequiredMixin, ListView):
    context_object_name = 'banklist'
    model = BankDetail
    queryset = BankDetail.objects.all()
    template_name = 'payment/bank_list.html'
    paginate_by = 30


class BankCreateView(LoginRequiredMixin, CreateView):
    form_class = BankRegisterForm
    template_name = 'payment/bank_register_form.html'
    success_url = reverse_lazy('payment:bank-list')
    # queryset= StudentDetail.objects.all()

    # success_url = '/'
    def form_valid(self, form):
        return super().form_valid(form)

# Payment Search 

def student_search_list(request):
    student = PaymentDetail.objects.all()
     # PAGINATOR METHOD
    page = request.GET.get('page', 1)
    paginator = Paginator(student, 30)
    try:
        payment = paginator.page(page)
    except PageNotAnInteger:
        payment = paginator.page(1)
    except EmptyPage:
        payment = paginator.page(paginator.num_pages)

    return render(request, 'payment/debtors.html', {'payment': payment })

# Define function to search student
def search(request):
    results = []

    if request.method == "GET":
        query = request.GET.get('search')

        if query == '':
            query = 'None'

        debtor = PaymentDetail.objects.filter(Q(student_detail__last_name__icontains=query) | Q(student_detail__current_class__icontains=query) | Q(installment_level__icontains=query) | Q(balance_pay__icontains=query) | Q(student_detail__first_name__icontains=query))

        
    return render(request, 'payment/search.html', {'query': query, 'debtor': results})