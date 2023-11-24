from django.db import models
from django.contrib.auth.models import User
from curriculum.models import Session
from students.models import StudentDetail
from django.conf import settings
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator 
# Create your models here.


class BankDetail(models.Model):
    name = models.CharField(max_length=150, blank=True)
    acc_number = models.CharField(max_length=20, blank=True)
    description = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering:['name']


class PaymentCategory(models.Model):
    name = models.CharField(max_length=150, blank=True, unique=True)
    description = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Payment Category'
        verbose_name_plural = 'Payment Categories'


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

    class Meta:
        ordering:['-session']
    

class PaymentDetail(models.Model):
    student_detail = models.ForeignKey(StudentDetail, on_delete=models.CASCADE, default=None, null=True)
    payee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, null=True)
    # Single payment
    payment_name = models.ForeignKey(PaymentChart, on_delete=models.CASCADE, default= None, related_name='payment_name')
    amount_paid = models.DecimalField(max_digits=15, decimal_places=2, default=0.0, null=True)
    bank_name = models.ForeignKey(BankDetail, on_delete=models.CASCADE, default=None, null=True)   
    description = models.CharField(max_length=200, blank=True)

    payment_date = models.DateField()  

    first = 'First_payment'
    second = 'Second_payment'
    third = 'Third_payment'
    fourth = 'Fourth_payment'
    complete = 'Complete_once'

    installment_level = [
        (first, 'First_payment'),
        (second, 'Second_payment'),
        (third, 'Third_payment'),
        (fourth, 'Fourth_payment'),
        (complete, 'Complete_once'),
    ]
    installment_level = models.CharField(max_length=50, choices=installment_level, default='select_installment')

    cash = 'cash'
    bank_deposit = 'bank_deposit'
    bank_transfer = 'bank_transfer'
    cheque = 'cheque'
    pos = 'pos'

    payment_methods = [
        (cash, 'cash'),
        (bank_deposit, 'bank_deposit'),
        (bank_transfer, 'bank_transfer'),
        (cheque, 'cheque'),
        (pos, 'pos'),
    ]
    payment_method = models.CharField(max_length=50, choices=payment_methods)  
    depositor = models.CharField(max_length=150) 
    # bank_name = models.CharField(max_length=150) 
    teller = models.CharField(max_length=150, blank=True)  
    # Discount for student
    discount = models.DecimalField(help_text='enter in %', max_digits=3, decimal_places=0, blank=True, null=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]) 
    # payment confirmation
    confirmed = models.BooleanField(default=False) 

    payment_recorded_date = models.DateField(auto_now_add=True)     

    class Meta:
        ordering = ['-payment_date' ]

    def __str__ (self):
        return f'{self.payee}'

    def get_absolute_url(self):
        return reverse('payment:payment_detail', kwargs={'id':self.id})

    @property
    def balance_pay(self):
       return self.payment_name.amount_due - self.amount_paid

    @property
    def discounted_amount_due(self):
       return self.payment_name.amount_due - (self.discount/100 * self.payment_name.amount_due)

    @property
    def discounted_balance_pay(self):
       return self.discounted_amount_due - self.amount_paid


       
    