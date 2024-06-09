from django.db import models
from users.models import User

# Create your models here.
class Task(models.Model):
    """
    title - Имя задачи
    description - Описание задачи
    status - Рабочий статус задачи (Черновик, В очереди, выполняется, срочно, выполнена)
    is_overdue - Метка, просрочена ли задача
    creation_time - Время создания задачи. (Перевод из черновика в очередь)
    work_time - Время, когда задача приобретает статус выполняется. (Переводится из очереди в актуальные)
    finish_by - Время, к которому нужно выполнить задачу
    finish_time - Время, когда пользователь выполнил задачу
    user - связка с пользователем
    """
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        QUEUE = 1, 'В Очереди'
        WORK = 2, 'Выполняется'
        URGENTLY = 3, 'Срочно'
        COMPLETED = 4, 'Выполнена'

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
    # Связка с пользователем
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
