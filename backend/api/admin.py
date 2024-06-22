from django.contrib import admin
from .models import Task

# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'phone', 'status', 'is_overdue')
    list_display_links = ('title', )
