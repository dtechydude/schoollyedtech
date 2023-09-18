from django.contrib import admin
from attendance.models import Attendance

# Register your models here.

class AttendanceAdmin(admin.ModelAdmin):
       
    list_display=('student_id', 'session', 'term', 'date_taken', 'morning_status', 'afternoon_status')

admin.site.register(Attendance, AttendanceAdmin)
