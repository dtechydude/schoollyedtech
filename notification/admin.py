from django.contrib import admin
from .models import Notification, SchoolCalendar

# Register your models here.
class NotificationAdmin(admin.ModelAdmin):
    list_display=('sender', 'date_sent', 'subject')


admin.site.register(Notification, NotificationAdmin)


class SchoolCalendarAdmin(admin.ModelAdmin):
    list_display=('event_name', 'event_date', 'duration')


admin.site.register(SchoolCalendar, SchoolCalendarAdmin)
