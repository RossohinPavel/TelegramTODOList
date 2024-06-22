from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Task(models.Model):
    """
    phone - Номер телефона пользователя
    title - Имя задачи
    description - Описание задачи
    status - Рабочий статус задачи (Черновик, В очереди, выполняется, срочно, выполнена)
    is_overdue - Метка, просрочена ли задача
    creation_time - Время создания задачи. (Перевод из черновика в очередь)
    work_time - Время, когда задача приобретает статус выполняется. (Переводится из очереди в актуальные)
    finish_by - Время, к которому нужно выполнить задачу
    finish_time - Время, когда пользователь выполнил задачу
    """
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        QUEUE = 1, 'В Очереди'
        WORK = 2, 'Выполняется'
        URGENTLY = 3, 'Срочно'
        COMPLETED = 4, 'Выполнена'

    # Связка с пользователем
    phone = models.CharField(max_length=11)
    # Контент задачи
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    # Статусы задачи
    status = models.SmallIntegerField(choices=Status.choices, default=Status.DRAFT)
    is_overdue = models.BooleanField(default=False)
    # Временые метки
    creation_time = models.DateTimeField(blank=True, null=True)
    work_time = models.DateTimeField(blank=True, null=True)
    finish_by = models.DateTimeField(blank=True, null=True)
    finish_time = models.DateTimeField(blank=True, null=True)
