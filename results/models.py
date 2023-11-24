from django.db import models
from django.contrib.auth.models import User
from users.models import Profile
from students.models import StudentDetail
from curriculum.models import Standard, Subject, Session
from django.conf import settings
from django.template.defaultfilters import slugify
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.urls import reverse, reverse_lazy



class Examination(models.Model):
    name = models.CharField(max_length=150, blank=True)
    description = models.CharField(max_length=150, blank=True)
    standard_name = models.ForeignKey(Standard, on_delete=models.CASCADE, help_text='Select Anonymous', blank=True, null=True)
  
    def __str__ (self):
        return f'{self.name}'
    


class MarkedSheet(models.Model):
    student = models.ForeignKey(StudentDetail, on_delete=models.CASCADE, blank=True, null=True, default=None)
    exam = models.ForeignKey(Examination, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE) 
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE)
    subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam_date = models.DateField(null=True)  
    cand_score = models.IntegerField(blank=True) 
    pass_mark =  models.IntegerField( blank=True) 
    remark = models.CharField(max_length=150, blank=True) 
    exam_paper = models.CharField(help_text='Paste link to marked sheet', max_length=300, blank=True)
    # file = models.FileField(upload_to='result', blank=True, verbose_name='upload marksheet')

    def __str__ (self):
        return f'{self.student.user.username} Marked Result'

    class Meta:
        verbose_name = 'Marked Sheet'
        verbose_name_plural = 'Marked Sheet'

    

class UploadResult(models.Model):
    student = models.ForeignKey(StudentDetail, on_delete=models.CASCADE, blank=True, null=True, default=None)
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE, blank=True, null=True, default=None) 
    exam = models.ForeignKey(Examination, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    # file = models.FileField(upload_to='result', blank=True, null=False, verbose_name='upload result')
    file = models.CharField(help_text='Paste Certificate Link', max_length=300, blank=True)
    remark = models.CharField(max_length=150, blank=True)

    def __str__ (self):    
        return f'{self.student}'

    class Meta:
        verbose_name = 'Certificate'
        verbose_name_plural = 'Certificate'




class ExamSubject(models.Model):
    subject_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    # image = models.ImageField(upload_to=save_subject_image, blank=True, verbose_name='Subject Image')
    description = models.TextField(max_length=500, blank=True)
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.subject_id)
        super().save(*args, **kwargs)


class ResultSheet(models.Model):
    student_detail = models.ForeignKey(StudentDetail, on_delete=models.CASCADE, blank=True, null=True, default=None)
    student_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, null=True, help_text='confirm student username')
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
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE)
    exam_date = models.DateField(null=True) 
    
    subject_1 = models.ForeignKey(ExamSubject, on_delete=models.CASCADE, related_name='subject_1', null=True, blank=True,)
    score_1ca = models.IntegerField(help_text='Enter C.A score', blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(40)]) 
    score_1exam = models.IntegerField(help_text='Enter Exam score', blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(60)]) 
    
    subject_2 = models.ForeignKey(ExamSubject, on_delete=models.CASCADE, related_name='subject_2', null=True, blank=True,)
    score_2ca = models.IntegerField(help_text='Enter C.A score', blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(40)]) 
    score_2exam = models.IntegerField(help_text='Enter Exam score', blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(60)]) 
    
    subject_3 = models.ForeignKey(ExamSubject, on_delete=models.CASCADE, related_name='subject_3', null=True, blank=True,)
    score_3ca = models.IntegerField(help_text='Enter C.A score', blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(40)]) 
    score_3exam = models.IntegerField(help_text='Enter Exam score', blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(60)]) 
   
    subject_4 = models.ForeignKey(ExamSubject, on_delete=models.CASCADE, related_name='subject_4', null=True, blank=True,)
    score_4ca = models.IntegerField(help_text='Enter C.A score', blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(40)]) 
    score_4exam = models.IntegerField(help_text='Enter Exam score', blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(60)]) 
    
    subject_5 = models.ForeignKey(ExamSubject, on_delete=models.CASCADE, related_name='subject_5', null=True, blank=True,)
    score_5ca = models.IntegerField(help_text='Enter C.A score', blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(40)]) 
    score_5exam = models.IntegerField(blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(60)]) 
    
    subject_6 = models.ForeignKey(ExamSubject, on_delete=models.CASCADE, related_name='subject_6', null=True, blank=True,)
    score_6ca = models.IntegerField(help_text='Enter C.A score', blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(40)]) 
    score_6exam = models.IntegerField(help_text='Enter Exam score', blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(60)]) 
    
    subject_7 = models.ForeignKey(ExamSubject, on_delete=models.CASCADE, related_name='subject_7', null=True, blank=True,)
    score_7ca = models.IntegerField(help_text='Enter C.A score', blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(40)]) 
    score_7exam = models.IntegerField(help_text='Enter Exam score', blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(60)]) 
    
    subject_8 = models.ForeignKey(ExamSubject, on_delete=models.CASCADE, related_name='subject_8', null=True, blank=True,)
    score_8ca = models.IntegerField(help_text='Enter C.A score', blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(40)]) 
    score_8exam = models.IntegerField(blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(60)]) 
    
    subject_9 = models.ForeignKey(ExamSubject, on_delete=models.CASCADE, related_name='subject_9', null=True, blank=True,)
    score_9ca = models.IntegerField(help_text='Enter C.A score', blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(40)]) 
    score_9exam = models.IntegerField(help_text='Enter Exam score', blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(60)]) 
    
    subject_10 = models.ForeignKey(ExamSubject, on_delete=models.CASCADE, related_name='subject_10', null=True, blank=True,)
    score_10ca = models.IntegerField(help_text='Enter C.A score', blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(40)]) 
    score_10exam = models.IntegerField(help_text='Enter Exam score', blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(60)]) 
    
    subject_11 = models.ForeignKey(ExamSubject, on_delete=models.CASCADE, related_name='subject_11', null=True, blank=True,)
    score_11ca = models.IntegerField(help_text='Enter C.A score', blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(40)]) 
    score_11exam = models.IntegerField(blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(60)]) 
    
    subject_12 = models.ForeignKey(ExamSubject, on_delete=models.CASCADE, related_name='subject_12', null=True, blank=True,)
    score_12ca = models.IntegerField(help_text='Enter C.A score', blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(40)]) 
    score_12exam = models.IntegerField(help_text='Enter Exam score', blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(60)]) 
   
    subject_13 = models.ForeignKey(ExamSubject, on_delete=models.CASCADE, related_name='subject_13', null=True, blank=True,)
    score_13ca = models.IntegerField(help_text='Enter C.A score', blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(40)]) 
    score_13exam = models.IntegerField(help_text='Enter Exam score', blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(60)]) 
    
    subject_14 = models.ForeignKey(ExamSubject, on_delete=models.CASCADE, related_name='subject_14', null=True, blank=True,)
    score_14ca = models.IntegerField(help_text='Enter C.A score', blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(40)]) 
    score_14exam = models.IntegerField(help_text='Enter Exam score', blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(60)]) 
    
    subject_15 = models.ForeignKey(ExamSubject, on_delete=models.CASCADE, related_name='subject_15', null=True, blank=True,)
    score_15ca = models.IntegerField(help_text='Enter C.A score', blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(40)]) 
    score_15exam = models.IntegerField(help_text='Enter Exam score', blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(60)]) 
    
    subject_16 = models.ForeignKey(ExamSubject, on_delete=models.CASCADE, related_name='subject_16', null=True, blank=True,)
    score_16ca = models.IntegerField(help_text='Enter C.A score', blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(40)]) 
    score_16exam = models.IntegerField(help_text='Enter Exam score', blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(60)]) 
   
    subject_17 = models.ForeignKey(ExamSubject, on_delete=models.CASCADE, related_name='subject_17', null=True, blank=True,)
    score_17ca = models.IntegerField(help_text='Enter C.A score', blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(40)]) 
    score_17exam = models.IntegerField(help_text='Enter Exam score', blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(60)]) 
    
    subject_18 = models.ForeignKey(ExamSubject, on_delete=models.CASCADE, related_name='subject_18', null=True, blank=True,)
    score_18ca = models.IntegerField(help_text='Enter C.A score', blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(40)]) 
    score_18exam = models.IntegerField(help_text='Enter Exam score', blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(60)]) 
    
    subject_19 = models.ForeignKey(ExamSubject, on_delete=models.CASCADE, related_name='subject_19', null=True, blank=True,)
    score_19ca = models.IntegerField(help_text='Enter C.A score', blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(40)]) 
    score_19exam = models.IntegerField(help_text='Enter Exam score', blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(60)]) 

    subject_20 = models.ForeignKey(ExamSubject, on_delete=models.CASCADE, related_name='subject_20', null=True, blank=True,)
    score_20ca = models.IntegerField(help_text='Enter C.A score', blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(40)]) 
    score_20exam = models.IntegerField(help_text='Enter Exam score', blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(60)]) 
    
    remark = models.CharField(max_length=150, blank=True, ) 
    class_teacher_comment = models.CharField(max_length=150, blank=True, null=True, default='auto-generated' ) 
    principal_comment = models.CharField(max_length=150, blank=True, null=True, default= 'auto-generated' )
    no_days_school_open = models.IntegerField(blank=True, default=0)
    no_days_present = models.IntegerField(blank=True, default=0)
    next_term_resume = models.DateField(blank=True, null=True) 
    publish = models.BooleanField(default=False) 

    class Meta:
        ordering = ['-exam_date']
    
        
    class Meta:
        verbose_name = 'Result Sheet'
        verbose_name_plural = 'Result Sheet'
    
    def get_absolute_url(self):
        return reverse('results:result-sheet', kwargs={'id':self.id})

    def __str__(self):
        st = StudentDetail.objects.get(id=self.student_detail_id)
        us = User.objects.get_or_create(id=self.student_id_id)
        # us = User.objects.get(id=self.student_id)
        # ex = Examination.objects.get_or_create(id=self.exam)
        return '%s ' % (st)


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
    def total_score_5(self):
        return self.score_5ca + self.score_5exam
    
    @property
    def total_score_6(self):
       return self.score_6ca + self.score_6exam
        
    @property
    def total_score_7(self):
       return self.score_7ca + self.score_7exam

    @property
    def total_score_8(self):
       return self.score_8ca + self.score_8exam

    @property
    def total_score_9(self):
       return self.score_9ca + self.score_9exam

    @property
    def total_score_10(self):
       return self.score_10ca + self.score_10exam

    @property
    def total_score_11(self):
       return self.score_11ca + self.score_11exam

    @property
    def total_score_12(self):
       return self.score_12ca + self.score_12exam

    @property
    def total_score_13(self):
       return self.score_13ca + self.score_13exam

    @property
    def total_score_14(self):
       return self.score_14ca + self.score_14exam

    @property
    def total_score_15(self):
       return self.score_15ca + self.score_15exam

    @property
    def total_score_16(self):
       return self.score_16ca + self.score_16exam

    @property
    def total_score_17(self):
       return self.score_17ca + self.score_17exam

    @property
    def total_score_18(self):
       return self.score_18ca + self.score_18exam

    @property
    def total_score_19(self):
       return self.score_19ca + self.score_19exam

    @property
    def total_score_20(self):
       return self.score_20ca + self.score_20exam

    @property
    def total_score_exam(self):
       return self.score_1exam + self.score_2exam + self.score_3exam + self.score_4exam + self.score_5exam + self.score_6exam + self.score_7exam + self.score_8exam + self.score_9exam + self.score_10exam + self.score_11exam + self.score_12exam + self.score_13exam + self.score_14exam + self.score_15exam + self.score_16exam + self.score_17exam + self.score_18exam + self.score_19exam + self.score_20exam

    @property
    def total_score_ca(self):
        return self.score_1ca + self.score_2ca + self.score_3ca + self.score_4ca + self.score_5ca + self.score_6ca + self.score_7ca + self.score_8ca + self.score_9ca + self.score_10ca + self.score_11ca + self.score_12ca + self.score_13ca + self.score_14ca + self.score_15ca + self.score_16ca + self.score_17ca + self.score_18ca + self.score_19ca + self.score_20ca
    
   
    @property
    def overall_total(self):
       return self.total_score_ca + self.total_score_exam

# getting total number of subjects taken
    @property
    def empty_fields_count(self):
        fields = ["subject_1", "subject_2", "subject_3", "subject_4", "subject_5", "subject_6", "subject_7", "subject_8", "subject_9", "subject_10", "subject_11", "subject_12", "subject_13", "subject_14", "subject_15", "subject_16", "subject_17", "subject_18", "subject_19", "subject_20"]
        empty_values = {"", None}
        empty_values_count = 0

        for field in fields:
            field_value = getattr(self, field)
            if field_value in empty_values:
                empty_values_count += 1
        return  20 - empty_values_count

    @property
    def overall_percentage(self):
        return (self.total_score_exam + self.total_score_ca) / self.empty_fields_count

    @property
    def no_days_absent(self):
        return self.no_days_school_open - self.no_days_present
        
 