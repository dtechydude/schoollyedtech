from django.contrib import admin
from .models import Post, Comment

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display=('author', 'date_posted', 'title')

admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display=('post',)


admin.site.register(Comment, CommentAdmin)
