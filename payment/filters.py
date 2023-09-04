import django_filters
from .models import PaymentDetail, PaymentChart
from django.contrib.auth.models import User

class PaymentFilter(django_filters.FilterSet):

    class Meta:
        model = PaymentDetail
        # # fields = '__all__'
        # fields = {'current_class': ['exact']}
        fields = {'payee', 'payment_name', 'payment_method'}

class MyPaymentFilter(django_filters.FilterSet):

    class Meta:
        model = PaymentDetail
        # # fields = '__all__'
        # fields = {'current_class': ['exact']}
        fields = {'payment_name', 'payment_method'}

class PaymentChartFilter(django_filters.FilterSet):

    class Meta:
        model = PaymentChart
        # # fields = '__all__'
        # fields = {'current_class': ['exact']}
        fields = {'session', 'payment_cat', 'term',}


class PaymentReportFilter(django_filters.FilterSet):

    class Meta:
        model = PaymentDetail
        # # fields = '__all__'
        # fields = {'current_class': ['exact']}
        fields = {'payment_name', 'payment_method'}
        

