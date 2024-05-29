from django.contrib import admin
from .models import Task


# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'completed')
    list_display_links = ('id', 'title')
    ordering = ('-execute_to', 'user', 'title')
