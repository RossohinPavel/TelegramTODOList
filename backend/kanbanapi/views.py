from rest_framework.request import Request
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .models import Task
from users.models import User
from .seryalizers import TaskSerializer

# Create your views here.
class TasksViewSet(ViewSet):
    """Класс представления для задач"""
    ALLOWED_FIELDS = ('title', 'description', 'work_time', 'finish_by', 'finish_time')

    def list(self, request: Request, phone: str):
        """Для получения/чтения списка записей."""
        queryset = Task.objects.filter(user__phone=phone)
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request: Request, phone: str):
        """Создание записи"""
        request.data['user'] = User.objects.get(phone=phone).id
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': 'ok', 'task_id': serializer.data['id']})

    def retrieve(self, request: Request, phone: str, pk=None):
        """Для получения/чтения одной записи по идентификатору pk (id)"""
        task = Task.objects.get(user__phone=phone, pk=pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    # def update(self, request, pk=None):
    #     pass

    # def partial_update(self, request: Request, phone: str, pk=None):
    #     task = Task.objects.get(user__phone=phone, pk=pk)
    #     for k, v in request.data.items():
    #         if k in 

    def destroy(self, request: Request, phone: str, pk=None):
        """Удаление записи"""
        task = Task.objects.get(user__phone=phone, pk=pk)
        task.delete()
        return Response({'status': 'ok'})

    def handle_exception(self, exc):
        """Обрабатываем возможные исключения"""
        return Response({'error': str(exc)})
