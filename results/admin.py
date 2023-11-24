from doctest import Example
from django.contrib import admin

from results.models import Examination, UploadResult, MarkedSheet, Session, ResultSheet, ExamSubject

# Register your models here.

class UploadResultAdmin(admin.ModelAdmin):
       
    list_display=('student', 'exam', 'session', 'file',)
    list_filter  = ['exam', 'exam']
    search_fields = ('student__user__username', 'student__last_name', 'student__first_name')
    raw_id_fields = ['student', 'standard', 'exam', 'session']

class ExamSubjectAdmin(admin.ModelAdmin):
       
    list_display=('subject_id', 'name',)

class ResultSheetAdmin(admin.ModelAdmin):
       
    list_display=('student_detail', 'session', 'exam',)
    list_filter  = ['student_detail__current_class']
    search_fields = ('student_detail__student_username', 'student_detail__last_name', 'student_detail__first_name')
    raw_id_fields = ['student_id', 'student_detail']

class ExaminationAdmin(admin.ModelAdmin):
       
    list_display=('name', 'standard_name',)

class MarkedSheetAdmin(admin.ModelAdmin):
       
    list_display=('student', 'session', 'exam',)
    list_filter  = ['session', 'exam']
    search_fields = ('student__user__username', 'student__last_name', 'student__first_name')
    raw_id_fields = ['student', 'standard', 'exam', 'session', 'subject_name']



admin.site.register(MarkedSheet, MarkedSheetAdmin)
admin.site.register(Examination, ExaminationAdmin)
admin.site.register(UploadResult, UploadResultAdmin)
admin.site.register(ExamSubject, ExamSubjectAdmin)
admin.site.register(ResultSheet, ResultSheetAdmin)
