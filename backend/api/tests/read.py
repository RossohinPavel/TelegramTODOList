from rest_framework.test import APITestCase
from .common import PATH, _get_currect_task, datetime


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
        path = f'{PATH}{pk}/'
        response = self.client.get(path)
        assert 'id' in response.data
        assert 'phone' in response.data
        assert 'title' in response.data
        assert 'description' in response.data
        assert 'status' in response.data
        assert 'creation_time' in response.data
        assert 'actual_time' in response.data
        assert 'finish_by' in response.data
        assert 'finish_time' in response.data
