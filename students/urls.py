from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from students import views as student_views 
from django.contrib.auth import views as auth_views
from students.views import (StudentListView,
                            StudentDetailView,
                            StudentCreateView,
                            StudentUpdateView,
                            StudentDeleteView,
                            MyStudentList,
                            StudentResultUpdateView,
)

app_name = 'students'

urlpatterns = [
   
    path('', student_views.studentlist, name="student-list"),
    path('student-register', student_views.studentregisterform, name="student-registration"),
    path('student-summary', student_views.student_summary, name="student-summary"),
    # path('pdf/<pk>/', student_views.student_render_pdf_view, name="student-pdf-view"),
    # path('student-list/', StudentListView.as_view(), name="all-students"),
    path('<int:id>/', StudentDetailView.as_view(), name="students-detail"), 
    path('new-student/', StudentCreateView.as_view(), name="students-create"),
    path('<int:id>/update/', StudentUpdateView.as_view(), name="students-update"),
    path('<int:id>/delete/', StudentDeleteView.as_view(), name="students-delete"),  

    path('<int:id>/result-update/', StudentResultUpdateView.as_view(), name="result-update"),

    path('pdf/<pk>/', student_views.student_render_pdf_view, name="student-pdf-view"),
    path('test-view/', student_views.render_pdf_view, name="test-view"),

    path('student-pdf', student_views.mystudent_pdf, name="student-pdf"),
    path('student-csv', student_views.mystudent_csv, name="student-csv"),

    #for my rest_framework
    path('api-auth/', MyStudentList.as_view(), name="apiview"),
    
 


]