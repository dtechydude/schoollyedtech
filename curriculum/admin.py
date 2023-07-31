from django.contrib import admin
from embed_video.admin import AdminVideoMixin

from curriculum.models import Lesson, Standard, Subject, Session, ClassGroup

# Register your models here.
class StandardAdmin(admin.ModelAdmin):
   
    list_display=('name', 'description')

class SubjectAdmin(admin.ModelAdmin):
       
    list_display=('subject_id', 'name', 'standard')

class LessonAdmin(admin.ModelAdmin):
       
    list_display=('lesson_id', 'standard', 'subject')

class SessionAdmin(admin.ModelAdmin):
   
    list_display=('name', 'description')

class ClassGroupAdmin(admin.ModelAdmin):
       
    list_display=('name', 'description',)
    

admin.site.register(Standard, StandardAdmin)
admin.site.register(ClassGroup, ClassGroupAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Session, SessionAdmin)





class MyModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass

