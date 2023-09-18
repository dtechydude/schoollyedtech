from django.db import models
from django.shortcuts import render
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from curriculum.models import Standard, ClassGroup
from django.urls import reverse
from staff.models import StaffProfile


# Create your models here.
class Badge(models.Model):
    name = models.CharField(max_length=50, blank=True)
    slug = models.SlugField(null=True, blank=True)
    description = models.CharField(max_length=120, blank=True)
    
    def __str__ (self):
        return f'{self.name}'

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name)
    #     super().save(*args, **kwargs)


class StudentDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='student_username', blank=True, null=True)
    student_username = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=15, blank=True)  
    current_class = models.ForeignKey(Standard, on_delete=models.CASCADE)
    class_group = models.ForeignKey(ClassGroup, on_delete=models.CASCADE)
    class_teacher = models.ForeignKey(StaffProfile, on_delete=models.CASCADE)
    badge =  models.ForeignKey(Badge, on_delete=models.CASCADE)
    is_prefect = models.BooleanField(default=False)

    day_student = 'day_student'
    boarder = 'boarder'

    student_types = [
        (day_student, 'day_student'),
        (boarder, 'boarder'),

    ]

    student_type = models.CharField(max_length=15, choices=student_types, default=day_student)

    address = models.CharField(max_length=120, blank=True, null=True)

    select = 'Select'
    southwest = 'SouthWest'
    southeast = 'SouthEast'
    southsouth = 'SouthSouth'
    northwest = 'NorthWest'
    northeast = 'NorthEast'
    northcentral = 'NorthCentral'
    
    region_origin = [
        ('Select', select),
        ('SouthWest', southwest),
        ('SouthEast', southeast),
        ('SouthSouth', southsouth),
        ('NorthWest', northwest),
        ('NorthEast', northeast),
        ('NorthCentral', northcentral),
    ]

    region_origin = models.CharField(max_length=20, choices=region_origin, default=select)

    female = 'female'
    male = 'male'
    select_gender = 'select_gender'
    
    gender_type = [
        ('female', female),
        ('male', male),
        ('select_gender', select_gender),
    ]

    gender= models.CharField(max_length=20, choices=gender_type, default= select_gender)

    dob = models.DateField(blank=True, null=True, verbose_name='Date of Birth (YYYY-MM-DD)')
    # class_on_admission = models.ForeignKey(Standard, on_delete=models.CASCADE)
    date_admitted = models.DateField( verbose_name='Admission date (MM-DD-YYYY)')
    # class_on_admission = models.CharField(max_length=50, blank=True, null=True, default=None)
    class_on_admission = models.ForeignKey(Standard, on_delete=models.CASCADE, related_name='studentdetails', verbose_name='class_on_admission') 
    
    # Guardian details here..
    guardian_name = models.CharField(max_length=60, blank=False)  
    guardian_address = models.TextField(max_length=120, blank=True)  
    guardian_phone = models.CharField(max_length=15, blank=True, null=True)
    guardian_email = models.CharField(max_length=30, blank=True, null=True)

    father = 'father'
    mother = 'mother'
    sister = 'sister'
    brother = 'brother'
    aunt = 'aunt'
    uncle = 'uncle'
    other = 'other'
    select = 'select'

    relationship = [
        (father, 'father'),
        (mother, 'mother'),
        (sister, 'sister'),
        (brother, 'brother'),
        (aunt, 'aunt'),
        (uncle, 'uncle'),
        (other, 'other'), 
        (select, 'select'), 

    ]

    relationship = models.CharField(max_length=25, choices=relationship, default=select)
    
    active = 'active'
    graduated = 'graduated'
    dropped = 'dropped'
    expelled = 'expelled'

    student_status = [
        (active, 'active'),
        (graduated, 'graduated'),
        (dropped, 'dropped'),
        (expelled, 'expelled'),

    ]

    student_status = models.CharField(max_length=15, choices=student_status, default=active)

    class Meta:
        ordering = ['user']

    def __str__ (self):
        return f'{self.user.username} - {self.last_name }  {self.first_name}'


    def get_absolute_url(self):
        return reverse('students:students-detail', kwargs={'id':self.id})

    





# Use for testing API call
class Mystudents(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=150, blank=True)  
    year = models.CharField(max_length=150, blank=True)   
    institution = models.CharField(max_length=150, blank=True)
    professional_body = models.CharField(max_length=150, blank=True)  
    academic = models.CharField(max_length=150, blank=True)  

    def __str__ (self):
        return f'{self.user.username} StudentAcademicInfo'



# Used on client's website
class AdmissionApplication(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False)
    email = models.CharField(max_length=150, blank=False, null=False)
    phone = models.CharField(max_length=150, blank=False, null=False)
    city = models.CharField(max_length=150, blank=False, null=False)
    last_class = models.CharField(max_length=150, blank=False, null=False)
    new_class = models.CharField(max_length=150, blank=False, null=False)
    application_date = models.DateField(auto_now=True)
    

    def __str__(self):
        return f'{self.name} - {self.application_date}'
