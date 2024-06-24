from rest_framework.test import APITestCase
from .common import PATH, _get_currect_task
from ..models import Task


class TitleRequiredTestCase(APITestCase):
    """Кейсы для проверки создания задачи."""

    @classmethod
    def setUpTestData(cls) -> None:
        cls._data = _get_currect_task()

    def setUp(self) -> None:
        """Создаем задачу"""
        self.response = self.client.post(PATH, data=self._data, format='json')

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
        assert response.data['message']
    
    def test_create_draft(self):
        """Проверяем ответ сервера на созданную задачу"""
        assert self.response.status_code == 200
        assert 'status' in self.response.data and self.response.data['status'] == 'ok'
        assert 'message' in self.response.data
        pk = self.response.data['message']
        assert isinstance(pk, int)
        # Сразу проверим, что запись приобрела статус 1 - черновик
        obj = Task.objects.get(pk=pk)
        assert obj.status == 1
