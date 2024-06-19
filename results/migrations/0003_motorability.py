# Generated by Django 3.2 on 2023-12-02 09:50

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MotorAbility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('honesty', models.IntegerField(blank=True, default=0, help_text='Honest', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('politeness', models.IntegerField(blank=True, default=0, help_text='Politeness', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('neatness', models.IntegerField(blank=True, default=0, help_text='Neatness', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('co_operation', models.IntegerField(blank=True, default=0, help_text='Co-operation', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('perseverance', models.IntegerField(blank=True, default=0, help_text='Perseverance', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('leadership', models.IntegerField(blank=True, default=0, help_text='Leadership', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('punctuality', models.IntegerField(blank=True, default=0, help_text='Enter Exam score', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('obedience', models.IntegerField(blank=True, default=0, help_text='Obedience', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('attentiveness', models.IntegerField(blank=True, default=0, help_text='Attentiveness', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('emotional_stability', models.IntegerField(blank=True, default=0, help_text='Emotional Stability', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('attitude', models.IntegerField(blank=True, default=0, help_text='Attitude', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('musical', models.IntegerField(blank=True, default=0, help_text='Musical', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('games', models.IntegerField(blank=True, default=0, help_text='Games', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('handwriting', models.IntegerField(blank=True, default=0, help_text='Handwriting', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('reading', models.IntegerField(blank=True, default=0, help_text='Reading', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('verbal_fluency', models.IntegerField(blank=True, default=0, help_text='Verbal Fluency', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('handling_tools', models.IntegerField(blank=True, default=0, help_text='Handling Tools', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('physical_education', models.IntegerField(blank=True, default=0, help_text='Physical Education', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('student_detail', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='results.resultsheet')),
            ],
        ),
    ]
