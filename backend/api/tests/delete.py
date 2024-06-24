from rest_framework.test import APITestCase
from .common import PATH, _get_currect_task


class DeleteTestCase(APITestCase):
    """Создание и удаление задачи"""

    @classmethod
    def setUpTestData(cls) -> None:
        cls._data = _get_currect_task()

    def setUp(self) -> None:
        """Создаем задачу"""
        self.response = self.client.post(PATH, data=self._data, format='json')

    def test_delete_task(self):
        """Удаляем задачу"""
        path = f'{PATH}{self.response.data['message']}/'
        response = self.client.delete(path)
        assert response.status_code == 200
        assert response.data['status'] == 'ok'
        assert response.data['message'].endswith('deleted.')
