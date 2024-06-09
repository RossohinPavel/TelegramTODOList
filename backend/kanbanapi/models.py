from django.db import models

# Create your models here.
class Task(models.Model):
    """
    title - Имя задачи
    description - Описание задачи
    status - Общий статус задачи (Черновик, В работе, завершена)
    work_status - Радочий статус задачи (В очереди, выполняется, срочно)
    is_overdue - Метка, просрочена ли задача
    creation_time - Время, когда задача была создана
    to_work_time - Время, когда задача приобретает статус выполняется. (Переводится из очереди в актуальные)
    finish_by - Закончить к этому времени
    user - связка с пользователем
    """
    # Контент задачи
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    # Статусы задачи
    status = models.IntegerField(blank=True, default=0)
    work_status = models.IntegerField(blank=True, null=True)
    is_overdue = models.BooleanField(blank=False)
    # Временые метки
    creation_time = models.DateTimeField(auto_now_add=True)
    time_to_work = models.DateTimeField(auto_now_add=True)
    finish_by = models.DateTimeField(auto_now_add=True)
    # Связка с пользователем
    user = models.ForeignKey()
