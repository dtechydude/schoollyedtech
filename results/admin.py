from doctest import Example
from django.contrib import admin

from results.models import Examination, UploadResult, Result, Session, ResultSheet, ExamSubject

# Register your models here.

class UploadResultAdmin(admin.ModelAdmin):
       
    list_display=('student', 'exam', 'session', 'file',)

class ExamSubjectAdmin(admin.ModelAdmin):
       
    list_display=('subject_id', 'name',)

class ResultSheetAdmin(admin.ModelAdmin):
       
    list_display=('student_id', 'session', 'exam',)



admin.site.register(Result)
admin.site.register(Examination)
# admin.site.register(Session)
admin.site.register(UploadResult, UploadResultAdmin)

# admin.site.register(ResultSheet)
admin.site.register(ExamSubject, ExamSubjectAdmin)
admin.site.register(ResultSheet, ResultSheetAdmin)
