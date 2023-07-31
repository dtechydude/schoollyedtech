import django_filters
from .models import PaymentDetail, PaymentChart
from django.contrib.auth.models import User

class PaymentFilter(django_filters.FilterSet):

    class Meta:
        model = PaymentDetail
        # # fields = '__all__'
        # fields = {'current_class': ['exact']}
        fields = {'student', 'payment_name', 'payment_date'}

class MyPaymentFilter(django_filters.FilterSet):

    class Meta:
        model = PaymentDetail
        # # fields = '__all__'
        # fields = {'current_class': ['exact']}
        fields = {'payment_name', 'payment_date'}

class PaymentChartFilter(django_filters.FilterSet):

    class Meta:
        model = PaymentChart
        # # fields = '__all__'
        # fields = {'current_class': ['exact']}
        fields = {'session', 'payment_cat', 'term',}
        
        

