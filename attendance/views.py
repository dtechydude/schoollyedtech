from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from attendance.models import Attendance
from attendance.forms import StudentAttendanceForm
# For Filter
from .filters import AttendanceFilter
from django_filters.views import FilterView
# For panigation
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#for pdf
from django.http import HttpResponse
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# for csv
import csv


@login_required
def student_attendance(request):
    if request.method == 'POST':
        attd_form = StudentAttendanceForm(request.POST)
      
        if attd_form.is_valid():
            attd_form.save()
            
            messages.success(request, f'Attendance taken. exit or enter another')
            return redirect('attendance:attendance_form')
    else:
         attd_form = StudentAttendanceForm()
    
       
            
    context = {
        'attd_form': attd_form,
       
   
    }

    return render(request, 'attendance/take-attendance.html', context)

@login_required
def attendance_view(request):
    attendance = Attendance.objects.all()
    attendance_filter = AttendanceFilter(request.GET, queryset=attendance) 
    attendance = attendance_filter.qs
    
    # PAGINATOR METHOD
    page = request.GET.get('page', 1)
    paginator = Paginator(attendance, 10)
    try:
        attendance = paginator.page(page)
    except PageNotAnInteger:
        attendance = paginator.page(1)
    except EmptyPage:
        attendance = paginator.page(paginator.num_pages)

    context = {
        'attendance' : Attendance.objects.all(),
        'attendance_filter': attendance_filter,
        'attendance': attendance

    }

    return render(request, 'attendance/attendance_view.html', context)



    
# Generate a PDF staff list
def attendance_pdf(request):
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
    attendance = Attendance.objects.all()

    # Create a blank list
        
    lines = [" Student Attendance Report"]

    for att in attendance:
        lines.append(""),
        lines.append("Username: " + str(att.student_id)),
        lines.append("Current Class: " + str(att.standard)),
        lines.append("Attandance Date: " + str(att.attendance_date)), 
        lines.append("Morning Status: " + str(att.morning_status)),
        lines.append("Afternoon Status: " + str(att.afternoon_status)),
        lines.append("-------------------------------------"),


    # loop
    for line in lines:
        textob.textLine(line)
    #fininsh up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    # Return something
    return FileResponse(buf, as_attachment=False, filename='attendance.pdf')


# Generate a CSV staff list
def attendance_csv(request):
    response = HttpResponse(content_type ='text/csv')
    response['Content-Disposition'] = 'attachment; filename=attendance.csv'
    
# Create a csv writer
    writer = csv.writer(response)

    attendance = Attendance.objects.all()
    
    # Add column headings to the csv files
    writer.writerow(['STUDENT ID', 'CLASS', 'ATT.DATE',
                    'MORNING', 'AFTERNOON', 'AUTHORIZED SIGN', 'DATE TAKEN',])


    # Loop thru and output
    for att in attendance:
        writer.writerow([att.student_id, att.standard,
                        att.attendance_date, att.morning_status, att.afternoon_status, att.authorized_sign, att.date_taken,])
        
    return response

