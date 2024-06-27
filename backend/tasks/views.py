from rest_framework.request import Request
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer, TasksListSerializer


def _get_response_dct(message, status: str = 'ok'):
    """Возвращает заготовленный словарь для ответа сервера."""
    return {'status': status, 'message': message}


# Create your views here.
class TasksAPIViewSet(ViewSet):
    """Класс представления для задач"""

    def list(self, request: Request, telegram_id: int):
        """Для получения/чтения списка записей"""
        # получим только актуальные задачки
        queryset = Task.objects.filter(user__telegram_id=telegram_id, status__gt=0)
        queryset = queryset.values('id', 'title', 'status')
        serializer = TasksListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request: Request, telegram_id: int, pk: int):
        """Для получения/чтения одной записи по идентификатору pk (id)"""
        task = Task.objects.get(user__telegram_id=telegram_id, pk=pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

#     def create(self, request: Request, phone: str):
#         """Создание записи"""
#         request.data['phone'] = phone
#         serializer = TaskSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(self.get_response_dict(serializer.data['id']))

#     # def update(self, request, pk=None):
#     #     pass

#     def partial_update(self, request: Request, phone: str, pk=None):
#         task = Task.objects.get(user__phone=phone, pk=pk)
#         # for k, v in request.data.items():
#         #     if k in 

#     def destroy(self, request: Request, phone: str, pk=None):
#         """Удаление записи"""
#         task = Task.objects.get(pk=pk, phone=phone)
#         name = task.title
#         task.delete()
#         return Response(self.get_response_dict(f'Task <{name}> deleted.'))

    def handle_exception(self, exc):
        """Обрабатываем возможные исключения"""
        return Response(_get_response_dct(str(exc), status='error'))
