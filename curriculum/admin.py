from django.contrib import admin
from embed_video.admin import AdminVideoMixin

from curriculum.models import Lesson, Standard, Subject, Session, ClassGroup

# Register your models here.


class StandardAdmin(admin.ModelAdmin):
   
    list_display=('name', 'description')

class SubjectAdmin(admin.ModelAdmin):
       
    list_display=('subject_id', 'name', 'standard')

class LessonAdmin(admin.ModelAdmin):
       
    list_display=(  'standard', 'subject', 'lesson_id', 'name' )
    list_filter = ['standard',]
    search_fields = ('standard__name', 'subject__name')
    raw_id_fields = ['created_by',]

class SessionAdmin(admin.ModelAdmin):
   
    list_display=('name', 'term', 'start_date', 'end_date')

class ClassGroupAdmin(admin.ModelAdmin):
       
    list_display=('name', 'description',)

# class TermAdmin(admin.ModelAdmin):
       
#     list_display=('name', 'session', 'start_date', 'end_date')
    

admin.site.register(Standard, StandardAdmin)
admin.site.register(ClassGroup, ClassGroupAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Session, SessionAdmin)
# admin.site.register(Term, TermAdmin)





class MyModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass

