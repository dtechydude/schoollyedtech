from doctest import Example
from django.contrib import admin

from results.models import Examination, UploadResult, Result, Session, ResultSheet

# Register your models here.

class UploadResultAdmin(admin.ModelAdmin):
       
    list_display=('student', 'exam', 'session', 'file',)




admin.site.register(Result)
admin.site.register(Examination)
# admin.site.register(Session)
admin.site.register(UploadResult, UploadResultAdmin)

admin.site.register(ResultSheet)
