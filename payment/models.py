from django.db import models
from django.contrib.auth.models import User
from curriculum.models import Session
from students.models import StudentDetail
from django.conf import settings
from django.core.validators import MinLengthValidator
# Create your models here.


class PaymentCategory(models.Model):
    name = models.CharField(max_length=150, blank=True)
    description = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f'{self.name}'


class PaymentChart(models.Model):
    name = models.CharField(max_length=150, blank=True)
    payment_cat = models.ForeignKey(PaymentCategory, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    first_term = 'first_term'
    second_term = 'second_term'
    third_term = 'third_term'
    others = 'others'

    term = [
        (first_term, 'first_term'),
        (second_term, 'second_term'),
        (third_term, 'third_term'),
        (others, 'others'),
    ]
    term = models.CharField(max_length=50, choices=term, blank=True) 
    amount_due = models.DecimalField(max_digits=15, decimal_places=2, default=0.0) 
    
    def __str__ (self):
        return f'{self.name}' 
    

class PaymentDetail(models.Model):
    payee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    payment_name = models.ForeignKey(PaymentChart, on_delete=models.CASCADE)
    amount_paid =models.DecimalField(max_digits=15, decimal_places=2, default=0.0) 
    
    payment_date = models.DateField()  

    cash = 'cash'
    bank_deposit = 'bank_deposit'
    cheque = 'cheque'
    pos = 'pos'

    payment_methods = [
        (cash, 'cash'),
        (bank_deposit, 'bank_deposit'),
        (cheque, 'cheque'),
        (pos, 'pos'),
    ]
    payment_method = models.CharField(max_length=50, choices=payment_methods)  
    depositor = models.CharField(max_length=150) 
    bank_name = models.CharField(max_length=150) 
    teller = models.CharField(max_length=150, blank=True) 
    description = models.CharField(max_length=200, blank=True)
    file = models.FileField(upload_to='payments', blank=True, verbose_name='upload receipt')
    confirmed = models.BooleanField(default=False) 
    payment_recorded_date = models.DateField(auto_now_add=True)     


    def __str__ (self):
        return f'{self.payee}'

    def get_absolute_url(self):
        return reverse('payment:payment_detail', kwargs={'id':self.id})
    