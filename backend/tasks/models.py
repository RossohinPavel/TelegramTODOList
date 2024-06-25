from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Task(models.Model):
    """Модель для описания задачи"""
    user = models.ForeignKey('users.User', models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True, default='')
    created_on = models.DateTimeField(auto_now_add=True)
    actual_on = models.DateTimeField()
    finish_by = models.DateTimeField()
    excuted_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-finish_by', 'actual_on']
    
    def clean(self):
        """Проверять надо только то, чтобы finish_by было больше actual_on"""
        if self.actual_on and self.finish_by and self.actual_on > self.finish_by:
            raise ValidationError({'finish_by': "finish_by attribute should be great then actual_on"})
        return super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)