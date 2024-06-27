from rest_framework.request import Request
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
# from .models import Task
# from django.db.models import Q
# from .serializers import TaskSerializer, TasksListSerializer


def _get_response_dct(message, status: str = 'ok'):
    """Возвращает заготовленный словарь для ответа сервера."""
    return {'status': status, 'message': message}


# Create your views here.
class TasksViewSet(ViewSet):
    """Класс представления для задач"""

#     def list(self, request: Request, phone: str):
#         """Для получения/чтения списка записей"""
#         query = Q(phone=phone)
#         if not request.GET.get('completed', False):
#             query &= Q(finish_time=None)
#         queryset = Task.objects.filter(query).values('id', 'title', 'status')
#         serializer = TasksListSerializer(queryset, many=True, partial=True)
#         return Response(serializer.data)

#     def retrieve(self, request: Request, phone: str, pk=None):
#         """Для получения/чтения одной записи по идентификатору pk (id)"""
#         task = Task.objects.get(pk=pk, phone=phone)
#         serializer = TaskSerializer(task)
#         return Response(serializer.data)

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

#     def handle_exception(self, exc):
#         """Обрабатываем возможные исключения"""
#         return Response(self.get_response_dict(str(exc), status='error'))


class CheckUserApi(APIView):
    """Подключение telegram к базе"""

    def get(self, request: Request):
        """Осуществляет проверку подключения telegram_id"""
        return Response({'test': 'ok'})

    def post(self, request: Request):
        """Вносит клиента в базу"""
        return Response({'test': 'ok'})

    def handle_exception(self, exc):
        return Response(_get_response_dct(str(exc), status='error'))
