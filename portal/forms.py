from tkinter import Widget
from django import forms
from curriculum.models import Standard, ClassGroup


class ClassRegisterForm(forms.ModelForm):

    class Meta:
        model = Standard
        fields = ('name', 'description',)

class ClassgroupRegisterForm(forms.ModelForm):

    class Meta:
        model = ClassGroup
        fields = ('name', 'description',)