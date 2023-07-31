from django.urls import path
from portal import views as portal_views 


app_name = 'portal'

urlpatterns = [
    path('home/', portal_views.portal_home, name="portal-home"),
    path('register-class/', portal_views.register_new_standard, name="register-class"),
    path('register-class-section/', portal_views.register_new_classgroup, name="register-classgroup"),

]
