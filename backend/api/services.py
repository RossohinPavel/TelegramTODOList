"""Здесь хранится логика обработки, в первую очередь сохранения информации в базы данных"""
from typing import Any
from django.core.exceptions import ValidationError


class ServiceMixin:
    """
    Абстрактный класс для работы с информацией, которая поступает в базу данных.
    Называть методы необходимо service_<attr> где <attr> - название атрибута, 
    которому присваивается значение.
    """
    __service_methods = None

    def __new__(cls, *args, **kwargs):
        if cls.__service_methods is None:
            # Сохраним в приватную переменную методы, 
            # которые будут впоследствии вызываться при валидации данных.
            cls.__service_methods = tuple(getattr(cls, n) for n in dir(cls) if n.startswith('service_'))
        return super().__new__(cls)
    
    # Even though the admin site invokes the method. 
    # The clean method is not invoked on save() or create() by default. 
    # So the best practice is to override the save method of the model and 
    # invoke the full_clean() method that under the hood calls clean and other validation hooks.
    
    def clean(self):
        print('---sss---')
        if not self.__service_methods:
            return
        for method in self.__service_methods:
            method(self)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class TaskServiceMixin(ServiceMixin):
    """Обслуживание модели Task"""

    def service_actual_time(self):
        """Проверка на то, что время окончания задачи больше времени постановки в работу"""
        print('---sss---')
        if self.actual_time and self.finish_by and self.actual_time >= self.finish_by:
            raise ValidationError({'actual_time': "Task's actual time should be less then finish by"})
