from django.db import models
from django.contrib.auth.models import User
from users.models import Profile
from students.models import StudentDetail
from curriculum.models import Standard, Subject, Session
from django.conf import settings
from django.template.defaultfilters import slugify

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


class ExamSubject(models.Model):
    subject_code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    # image = models.ImageField(upload_to=save_subject_image, blank=True, verbose_name='Subject Image')
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.subject_id)
        super().save(*args, **kwargs)


class ResultSheet(models.Model):
    student_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, null=True)
    student_detail = models.ForeignKey(StudentDetail, on_delete=models.CASCADE, blank=True, null=True, default=None)
    exam = models.ForeignKey(Examination, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE) 
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE)
    exam_date = models.DateField(null=True) 
    subject_1 = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject_1')
    score_1ca = models.IntegerField(blank=True) 
    score_1exam = models.IntegerField(blank=True) 
    subject_2 = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject_2')
    score_2ca = models.IntegerField(blank=True) 
    score_2exam = models.IntegerField(blank=True) 
    subject_3 = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject_3')
    score_3ca = models.IntegerField(blank=True) 
    score_3exam = models.IntegerField(blank=True) 
    subject_4 = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject_4')
    score_4ca = models.IntegerField(blank=True) 
    score_4exam = models.IntegerField(blank=True) 
    remark = models.CharField(max_length=150, blank=True) 
    
    def __str__ (self):
        return f'{self.student_id.username} Result'

    def get_absolute_url(self):
        return reverse('results:result-sheet', kwargs={'id':self.id})

    @property
    def total_score_1(self):
       return self.score_1ca + self.score_1exam

    @property
    def total_score_2(self):
       return self.score_2ca + self.score_2exam

    @property
    def total_score_3(self):
       return self.score_3ca + self.score_3exam
    
    @property
    def total_score_4(self):
       return self.score_4ca + self.score_4exam

    @property
    def total_score_exam(self):
       return self.score_1exam + self.score_2exam + self.score_3exam + self.score_4exam

    @property
    def total_score_exam_average(self):
       return self.total_score_exam / 100

