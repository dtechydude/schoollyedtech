from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, ListView, DeleteView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect, HttpResponse
from notification.models import Notification
from .forms import MailForm, EventRegisterForm, EventUpdateForm
from django.contrib.auth.models import User
from django.contrib import messages
import os
from .models import SchoolCalendar
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



class NotificationListView(ListView):
    model = Notification
    template_name = 'notification/mail_list.html'
    context_object_name = 'notification'
    ordering = ['-date_sent']


class NotificationDetailView(DetailView):
    model = Notification
    template_name = 'notification/mail_detail.html'
    context_object_name = 'mails'


class NotificationCreateView(CreateView):
    form_class = MailForm
    context_object_name = 'notification'
    model = Notification
    template_name = 'notification/send_mail.html'

    def form_valid(self, form, *args, **kwargs):
        form.instance.sender = self.request.user
        return super().form_valid(form)



class NotificationDeleteView(DeleteView):
    model = Notification
    template_name = 'notification/notification_detail.html'


@login_required
def view_self_notification(request, **kwargs):
# this issue was solved by me.
    try:     
        mymail = Notification.objects.filter(recipient=User.objects.get(username=request.user))
    
        context = {
            'mymail':mymail
            
        }    
    
        return render(request, 'notification/view_self_mail.html', context)

    except Notification.DoesNotExist:
        return HttpResponse('You are not a registered')
        

# FUNCTION FOR DOWNLOADING FILE
def download(request,path):
    file_path=os.path.join(settings.MEDIA_ROOT,path)
    if os.path.exists(file_path):
        with open(file_path, 'rb')as fh:
            response=HttpResponse(fh.read(),content_type="application/file")
            response['Content-Disposition']='inline;filename='+os.path.basename(file_path)
            return response

    raise Http404


@login_required
def school_calendar(request):

    queryset = SchoolCalendar.objects.all().order_by("-id")
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 4)
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)
    
    context = {
       
        'queryset': queryset,
        'events':events,
    }
    return render(request, 'notification/school_calendar.html', context)


@login_required
def school_calendar_form(request):
    if request.method == 'POST':
        
        event_form = EventRegisterForm(request.POST)
        if event_form.is_valid():
           
            event_form.save()
            messages.success(request, f'New event addedd successfully!')
            return redirect('notification:calendar')
    else:
      
        event_form = EventRegisterForm

    context = {
        
        'event_form': event_form,
    }

    return render(request, 'notification/school_calendar_form.html', context)

    
class EventUpdateView(LoginRequiredMixin, UpdateView):
    form_class = EventUpdateForm
    template_name = 'staff/staff_update_form.html'
    success_url = reverse_lazy('notification:calendar')


class EventDetailView(LoginRequiredMixin, UpdateView):
  
    template_name = 'staff/staff_update_form.html'

class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = SchoolCalendar
    template_name = 'notification/school_calendar_delete.html'
    success_url = reverse_lazy('notification:calendar')
    
   