from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class TaskManager(models.Manager):

    # Шпаргалка по статусам
    # COMPLETED = 0, 'Выполнена'
    # QUEUE = 1, 'В Очереди'
    # ACTUAL = 2, 'Актуальная'
    # OVERDUE = 3, 'Просрочена'

    def get_queryset(self) -> models.QuerySet:
        """Динамически формирует статус задачи"""
        now = timezone.now()
        queryset = super().get_queryset().annotate(
            status=models.Case(
                # Если проставлено finish_time, значит задача выполнена
                models.When(~models.Q(excuted_on=None), then=models.Value(0)),
                # Если <сейчас> меньше постановки задачи в работу - задача в очереди
                models.When(actual_on__gt=now, then=models.Value(1)),
                # Если <сейчас> меньше finish_by - задача актуальная
                models.When(finish_by__gt=now, then=models.Value(2)),
                # Если <сейчас> больше finish_by - задача просрочена
                models.When(finish_by__lte=now, then=models.Value(3)),
                default=models.Value(-1)
            )
        )
        return queryset


class Task(models.Model):
    """Модель для описания задачи"""
    user = models.ForeignKey('users.User', models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True, default='')
    created_on = models.DateTimeField(auto_now_add=True)
    actual_on = models.DateTimeField()
    finish_by = models.DateTimeField()
    excuted_on = models.DateTimeField(blank=True, null=True)
    
    # Менеджер модели
    objects = TaskManager()

    class Meta:
        ordering = ['-finish_by', 'actual_on']
    
    def __str__(self) -> str:
        return f"{self.user.username}'s <{self.title}>"
    
    def clean(self):
        """Проверять надо только то, чтобы finish_by было больше actual_on"""
        if self.actual_on and self.finish_by and not self.finish_by > self.actual_on:
            raise ValidationError({'finish_by': "finish_by attribute should be great then actual_on"})
        return super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
