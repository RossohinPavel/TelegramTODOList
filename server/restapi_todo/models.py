from django.db import models
import datetime

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    creation = models.DateTimeField(auto_now_add=True)
    execute_to = models.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(days=1))
    completed = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-execute_to']
