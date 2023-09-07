from django.contrib import admin
from pages.models import SchoolDetail


# Register your models here.
class SchoolDetailAdmin(admin.ModelAdmin):
   
    list_display=('name', 'phone', 'email',)