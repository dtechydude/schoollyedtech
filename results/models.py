from django.db import models
from django.contrib.auth.models import User
from users.models import Profile
from students.models import StudentDetail
from curriculum.models import Standard, Subject, Session

# Create your models here.
# class Session(models.Model):
#     name = models.CharField(max_length=150)
  
#     def __str__ (self):
#         return f'{self.name} session'


class Examination(models.Model):
    name = models.CharField(max_length=150, blank=True)
    description = models.CharField(max_length=150, blank=True)
    standard_name = models.ForeignKey(Standard, on_delete=models.CASCADE)
  
    def __str__ (self):
        return f'{self.name}'
    


class Result(models.Model):
    student = models.ForeignKey(StudentDetail, on_delete=models.CASCADE, blank=True, null=True, default=None)
    exam = models.ForeignKey(Examination, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE) 
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE)
    subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam_date = models.DateField(null=True)  
    cand_score = models.IntegerField(blank=True) 
    pass_mark =  models.IntegerField( blank=True) 
    remark = models.CharField(max_length=150, blank=True) 
    file = models.FileField(upload_to='result', blank=True, verbose_name='upload marksheet')

    def __str__ (self):
        return f'{self.student.user.username} Result'

    

class UploadResult(models.Model):
    student = models.ForeignKey(StudentDetail, on_delete=models.CASCADE, blank=True, null=True, default=None)
    description = models.CharField(max_length=150, blank=True)
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE, blank=True, null=True, default=None) 
    exam = models.ForeignKey(Examination, on_delete=models.CASCADE)
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

    term = models.CharField(max_length=15, choices=term, default=others)
    file = models.FileField(upload_to='result', blank=True, null=False, verbose_name='upload result')

    def __str__ (self):    
        return f'{self.student}'

    # def file_link(self):
    #     if self.file:
    #         return format_html("<a href='%s'>download</a>" % (self.file.url,))
    #     else:
    #         return "No attachment"
    
    # file_link.allow_tags = True
