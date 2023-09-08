from django.contrib import admin
from exams.models import SchoolDetail

# Register your models here.
class SchoolDetailAdmin(admin.ModelAdmin):
   
    list_display=('name',)