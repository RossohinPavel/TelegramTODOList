"""Здесь хранится логика обработки, в первую очередь сохранения информации в базы данных"""
from typing import Any
from django.core.exceptions import ValidationError


class ServiceMixin:
    """
    Абстрактный класс для работы с информацией, которая поступает в базу данных.
    Называть методы необходимо service_<attr> где <attr> - название атрибута, 
    которому присваивается значение.
    """
    __methods = None

    def __new__(cls, *args, **kwargs):
        if cls.__methods is None:
            # Сохраним в приватную переменную методы, 
            # которые будут впоследствии вызываться при валидации данных.
            pref = 'service_'
            cls.__methods = {n.replace(pref, ''): getattr(cls, n) for n in dir(cls) if n.startswith(pref)}
        return super().__new__(cls)
    
    def __setattr__(self, name: str, value: Any) -> None:
        if value is not None and name in self.__methods:
            value = self.__methods[name](self, value)
        return super().__setattr__(name, value)


class TaskServiceMixin(ServiceMixin):
    """Обслуживание модели Task"""

    def service_finish_by(self, value):
        """Проверка на то, что время окончания задачи больше времени постановки в работу"""
        if value <= self.work_time:
            raise ValidationError({'finish_by': 'Finish time cannot be less to do at work'})
        return value
