from django.contrib import admin

from staff.models import Department, StaffCategory, StaffProfile

# Register your models here.
class StaffProfileAdmin(admin.ModelAdmin):
       
    list_display=('staff_username', 'cat_name', 'class_in_charge')

admin.site.register(StaffCategory)
admin.site.register(StaffProfile, StaffProfileAdmin)
# admin.site.register(StaffAcademicInfo)
admin.site.register(Department)
