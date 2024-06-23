from django.db import models
from django.utils import timezone


class TaskManager(models.Manager):

    # Шпаргалка по статусам
    # COMPLETED = 0, 'Выполнена'
    # DRAFT = 1, 'Черновик'
    # QUEUE = 2, 'В Очереди'
    # ACTUAL = 3, 'Актуальная'
    # OVERDUE = 4, 'Просрочена'

    def get_queryset(self) -> models.QuerySet:
        """Динамически формирует статус задачи"""
        now = timezone.now()
        queryset = super().get_queryset().annotate(
            status=models.Case(
                # Если проставлено finish_time, значит задача выполнена
                models.When(~models.Q(finish_time=None), then=models.Value(0)),
                # Если не определено creation_time - задача в статусе черновика
                models.When(creation_time=None, then=models.Value(1)),
                # Если <сейчас> меньше постановки задачи в работу - задача в очереди
                models.When(actual_time__gt=now, then=models.Value(2)),
                # Если <сейчас> меньше finish_by - задача актуальная
                models.When(finish_by__gt=now, then=models.Value(3)),
                # Если <сейчас> больше finish_by - задача просрочена
                models.When(finish_by__lte=now, then=models.Value(4)),
                default=models.Value(-1)
            )
        )
        return queryset


# Create your models here.
class Task(models.Model):
    """
    phone - Номер телефона пользователя
    title - Имя задачи
    description - Описание задачи
    creation_time - Время создания задачи. (Перевод из черновика в очередь)
    actual_time - Время, когда задача приобретает статус выполняется. (Переводится из очереди в актуальные)
    finish_by - Время, к которому нужно выполнить задачу
    finish_time - Время, когда пользователь выполнил задачу
    --status - вычисляемое поле через менеджер tasks_manager
    """
    # objects = models.Manager()      # Оставим стандартный менеджер
    objects = TaskManager()   # Кастомный, с вычисляемым полем status

    # Связка с пользователем
    phone = models.CharField(max_length=11)
    # Контент задачи
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    # Временые метки
    creation_time = models.DateTimeField(blank=True, null=True)
    actual_time = models.DateTimeField(blank=True, null=True)
    finish_by = models.DateTimeField(blank=True, null=True)
    finish_time = models.DateTimeField(blank=True, null=True)
