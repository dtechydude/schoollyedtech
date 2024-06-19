from django.contrib import admin
from payment.models import PaymentCategory, PaymentChart, PaymentDetail, BankDetail

# Register your models here.
class PaymentCategoryAdmin(admin.ModelAdmin):
    list_display=('name', 'description',)

class PaymentChartAdmin(admin.ModelAdmin):

    list_display=('name', 'payment_cat', 'amount_due', 'session', 'term')
    list_filter  = ['payment_cat',]
    search_fields = ('session', 'term')

class PaymentDetailAdmin(admin.ModelAdmin):

    list_display=('payee', 'payment_name', 'amount_paid', 'payment_date', 'confirmed')
    list_filter  = ['student_detail__current_class']
    search_fields = ('student_detail__user__username', 'student_detail__last_name', 'student_detail__first_name')
    raw_id_fields = ['payee', 'student_detail', 'payment_name']


class BankDetailAdmin(admin.ModelAdmin):

    list_display=('name', 'acc_number', 'description',)



admin.site.register(PaymentCategory, PaymentCategoryAdmin)
admin.site.register(PaymentChart, PaymentChartAdmin)
admin.site.register(PaymentDetail, PaymentDetailAdmin)
admin.site.register(BankDetail, BankDetailAdmin)
