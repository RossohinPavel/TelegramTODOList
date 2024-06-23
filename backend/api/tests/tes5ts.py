from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from ..models import Task as TaskModel
from datetime import datetime, timedelta



# Create your tests here.
class TitleRequiredTestCase(APITestCase):
    """Кейсы для проверки создания задачи."""

    def test_title_required(self):
        """Тест на пустой заголовок"""
        response = self.client.post(PATH, data={"title": ""}, format='json')
        # Сервер отвечает без ошибок и посылает информацию в status
        assert response.status_code == 200
        assert 'status' in response.data 
        assert response.data['status'] == 'error'

    def test_create_minimal_draft(self):
        """Для создания черновика достаточно передать title"""
        data = {"title": "test"}
        response = self.client.post(PATH, data=data, format='json')
        assert response.status_code == 200
        assert response.data['status'] == 'ok'


class CreateAndDeleteTestCase(APITestCase):
    """Создание и удаление задачи"""

    @classmethod
    def setUpTestData(cls) -> None:
        cls._data = _get_currect_task()

    def setUp(self) -> None:
        """Создаем задачу"""
        self.response = self.client.post(PATH, data=self._data, format='json')
    
    def test_create_minimal_draft(self):
        """Проверяем ответ сервера на созданную задачу"""
        assert self.response.status_code == 200
        assert 'status' in self.response.data and self.response.data['status'] == 'ok'
        assert 'message' in self.response.data
        pk = self.response.data['message']
        assert isinstance(pk, int)
        # Сразу проверим, что запись приобрела статус 0 - черновик
        obj = TaskModel.objects.get(pk=pk)
        assert obj.status == 0

    # def test_delete_task(self):
    #     """Удаляем задачу"""
    #     pk = self.response.data['message']
    #     path = 1
        # response = self.client.delete(PATH, data=data, format='json')


class ListAndRetrieveTestCase(APITestCase):
    """Кейсы для проверки получения списка задач"""

    def setUp(self) -> None:
        # Создадим 10 задач обычных и 10 выполненных
        for i in range(20):
            data = _get_currect_task()
            if i > 9:
                data['finish_time'] = datetime.now()
            self.client.post(PATH, data=data, format='json')
    
        self.response = self.client.get(PATH)

    def test_1_list(self):
        """
        Получение списка задачек. Выдавать должен только активные 
        т.е. у которых не проставлено finish_time
        """
        assert self.response.status_code == 200
        assert 'status' not in self.response.data
        assert isinstance(self.response.data, list)
        assert len(self.response.data) == 10
    
    def test_2_list_with_completed(self):
        """Выдача с выполненными"""
        response = self.client.get(PATH, QUERY_STRING='completed=True')
        assert 'status' not in response.data
        assert isinstance(response.data, list)
        assert len(response.data) == 20

    def test_3_len_of_task_in_list(self):
        """Информация по задаче в списке должна быть ограничена 3 полями id, title, status"""
        # Получаем эти задачки
        task = self.response.data[0]
        assert isinstance(task, dict)
        assert len(task) == 3
        assert 'id' in task
        assert 'title' in task
        assert 'status' in task

    def test_4_retrieve(self):
        """Получение одной задачки"""
        pk = self.response.data[0]['id']
        response = self.client.get(PATH)
        pk = response.data[0]['id']
        response = self.client.get(f'{PATH}/{pk}')
