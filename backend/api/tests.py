from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from .models import Task as TaskModel
from datetime import datetime, timedelta


PATH = reverse('tasks-list', kwargs={'phone': '89998887766'})

# Create your tests here.
class CreateTaskTestCase(APITestCase):
    """Кейсы для проверки создания задачи."""

    def test_title_required(self):
        """Заголовок задачи необходим"""
        response = self.client.post(PATH)
        assert response.status_code == 400
        assert 'title' in response.data
    
    def test_create_minimal_draft(self):
        """Для создания черновика достаточно передать title"""
        data = {"title": "test"}
        response = self.client.post(PATH, data=data, format='json')
        assert response.status_code == 200
        assert response.data['status'] == 'ok'
        # Сразу проверим, что запись приобрела статус 0 - черновик
        obj = TaskModel.objects.get(pk=response.data['id'])
        assert obj.status == 0
    
    @staticmethod
    def _get_currect_task(wt_shift: int = 1, fb_shift: int = 2) -> dict:
        """
        Возвращает словарь заполненной задачей.
        параметры shift - сдвиг по времени в часах
        wt_shift - для передачи задачи из очереди в актуальное
        fb_shift - для времени - закончить к
        """
        # Содержит только те поля, которые пользователь может менять непосредственно.
        dct = {
            'title': 'title',
            'description': 'description',
            'work_time': datetime.now() + timedelta(wt_shift),
            'finish_by': datetime.now() + timedelta(fb_shift),
        }
        return dct


class GetTasksInformationTestCase(TestCase):
    """Кейсы для проверки получения информации по задачам"""

    def test_get_list(self):
        """Проверка выдачи списка задач"""
        response = self.client.get(PATH)
        assert response.status_code == 200
    
    def test_get_list_with_completed(self):
        """Проверка выдачи списка задач вместе с выполненными"""
        response = self.client.get(PATH)
        assert response.status_code == 200
