from django import forms
from .models import Attendance


class StudentAttendanceForm(forms.ModelForm):
    
    class Meta:
        model = Attendance
        fields = ['student_id', 'session', 'term', 'morning_status', 'afternoon_status', 'attendance_date', 'authorized_sign']
        widgets = {
            'attendance_date': forms.DateInput(
                format=('%d/%m/%Y'),
                attrs={'class': 'form-control', 
                       'placeholder': 'Select a date',
                       'type': 'date'  # <--- IF I REMOVE THIS LINE, THE INITIAL VALUE IS DISPLAYED
                      }),
        }


   
