from django.contrib import admin
from .models import QuizResult

# Register your models here.
class QuizResultAdmin(admin.ModelAdmin):
       
    list_display=('quiz', 'user', 'score',)

admin.site.register(QuizResult, QuizResultAdmin)
