from django.contrib import admin

from students.models import Mystudents, StudentDetail, Badge

class StudentAdmin(admin.ModelAdmin):
       
    list_display=('user', 'current_class', 'date_admitted', 'guardian_phone')

class BadgeAdmin(admin.ModelAdmin):
       
    list_display=('name', 'description',)



# class StudentProfileAdmin(admin.ModelAdmin):
       
#     list_display=('user', 'current_class', 'date_admitted', 'parent_phone')


# Register your models here.
admin.site.register(StudentDetail, StudentAdmin)
admin.site.register(Badge, BadgeAdmin)

# admin.site.register(StudentProfile, StudentProfileAdmin)
