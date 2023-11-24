import django_filters
from .models import UploadResult, ResultSheet
from django.contrib.auth.models import User

class MyresultFilter(django_filters.FilterSet):

    class Meta:
        model = UploadResult
        # # fields = '__all__'
        # fields = {'current_class': ['exact']}
        fields = {'exam', 'session',}
        

class MyResultSheetFilter(django_filters.FilterSet):

    class Meta:
        model = ResultSheet
        # # fields = '__all__'
        # fields = {'current_class': ['exact']}
        fields = {'exam', 'session',}
        

class ResultSheetFilter(django_filters.FilterSet):

    class Meta:
        model = ResultSheet
        # # fields = '__all__'
        # fields = {'current_class': ['exact']}
        fields = {'exam', 'session', 'term'}
        