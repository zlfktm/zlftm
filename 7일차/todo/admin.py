from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from todo.models import Todo, Comment

admin.site.register(Comment)

class CommentInline(admin.TabularInline):
    model = Comment
    fields = ['message', 'user']
    extra = 1

@admin.register(Todo)
class TodoAdmin(SummernoteModelAdmin):
    list_display = ['id', 'title', 'is_completed','completed_image', 'created_at','updated_at']
    list_display_links = ['title']
    list_filter = ['title','is_completed']

    summernote_fields = ['description',]

    inlines = [
        CommentInline,
    ]

