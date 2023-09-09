from django.contrib import admin
from users.models import Profile


class UserProfileAdmin(admin.ModelAdmin):
       
    list_display=('user', 'code', 'user_type')

# Register your models here.
admin.site.register(Profile, UserProfileAdmin)


# Register your models here.

# # Hide first name and last name from admin panel
# class UserAdminCustom(UserAdmin):

#     def get_fieldsets(self, request, obj=None):
#         fieldsets = super().get_fieldsets(request, obj)
#         new = []
#         for name, fields_dict in fieldsets:
#             if fields_dict['fields'] == ('first_name', 'last_name',):
#                 fields_dict['fields'] = ('email',)
#             new.append((name, fields_dict))
#         return new

