from tkinter import Widget
from django import forms
from curriculum.models import Standard, ClassGroup, Session
from results.models import Examination


class ClassRegisterForm(forms.ModelForm):

    class Meta:
        model = Standard
        fields = ('name', 'description',)

class ClassgroupRegisterForm(forms.ModelForm):

    class Meta:
        model = ClassGroup
        fields = ('name', 'description',)

class SessionRegisterForm(forms.ModelForm):

    class Meta:
        model = Session
        fields = ('name', 'description',)


class ExamRegisterForm(forms.ModelForm):

    class Meta:
        model = Examination
        fields = ('name', 'description',)