from django.db import models
from django.contrib.auth.models import User
from curriculum.models import Session
from students.models import StudentDetail
from django.conf import settings
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator 
from django.db.models import F, Sum, Q


class BankDetail(models.Model):
    name = models.CharField(max_length=150, blank=True)
    acc_number = models.CharField(max_length=20, blank=True)
    description = models.CharField(max_length=150, blank=True, verbose_name='Account Name')

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

    first_term = 'First Term'
    second_term = 'Second Term'
    third_term = 'Third Term'
    others = 'Others'

    term = [
        (first_term, 'First Term'),
        (second_term, 'Second Term'),
        (third_term, 'Third Term'),
        (others, 'Others'),
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

    first = 'First Payment'
    second = 'Second Payment'
    third = 'Third Payment'
    fourth = 'Fourth Payment'
    complete = 'Lump Sum'

    installment_level = [
        (first, 'First Payment'),
        (second, 'Second Payment'),
        (third, 'Third Payment'),
        (fourth, 'Fourth Payment'),
        (complete, 'Lump Sum'),
    ]
    installment_level = models.CharField(max_length=50, choices=installment_level, default='select_installment')

    cash = 'Cash'
    bank_deposit = 'Bank Deposit'
    bank_transfer = 'Bank Transfer'
    cheque = 'Cheque'
    pos = 'POS'

    payment_methods = [
        (cash, 'Cash'),
        (bank_deposit, 'Bank Deposit'),
        (bank_transfer, 'Bank Transfer'),
        (cheque, 'Cheque'),
        (pos, 'POS'),
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


    # for getting total number of payments a student made
    @property
    def no_of_payments(request):
      return PaymentDetail.objects.filter(student_detail = request.student_detail).count()

    # @property
    # def total_of_payments(request):
    #     return PaymentDetail.objects.filter(student_detail=request.student_detail).value('student_detail__student_username').annotate(total_payment=Sum('amount_paid')))
    #                                         # (payee=User.objects.get(username=request.user))


       
    