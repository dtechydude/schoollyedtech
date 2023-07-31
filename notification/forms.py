from django import forms
from.models import Notification, SchoolCalendar



class MailForm(forms.ModelForm):
   
    class Meta:
        
        model = Notification
        fields = ('recipient', 'subject', 'content', 'attachement')


# class ReplyMailForm(forms.ModelForm):
#     class Meta:
#         model = ReplyMailForm
#         fields = ('reply_body',)

#         widgets = {
#             'reply_body': forms.Textarea(attrs={'class':'form-control', 'rows':2, 'cols':10}),

class EventRegisterForm(forms.ModelForm):
   
    class Meta:
        
        model = SchoolCalendar
        fields = ('event_name', 'event_description', 'event_date', 'duration',)

class EventUpdateForm(forms.ModelForm):
   
    class Meta:
        
        model = SchoolCalendar
        fields = ('event_name', 'event_description', 'event_date', 'duration',)