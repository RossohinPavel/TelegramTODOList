from django.urls import reverse
from rest_framework.test import APITestCase
from .models import User


# Create your tests here.
class TelegramExtensionTestCase(APITestCase):
    check_user_url = reverse('check_user_api')
    set_telegram_id_url = reverse('set_telegram_id_api')
    data = {'phone': '79998887766', 'telegram_id': 1}

    def test_set_correct_phone(self):
        """Отправка корректного номера"""
        user = User.objects.create(phone=self.data['phone'])
        response = self.client.post(self.set_telegram_id_url, data=self.data)
        assert response.status_code == 200

    def test_set_wrong_phone(self):
        """Отправка телефона, которого нет в базе"""
        response = self.client.post(self.set_telegram_id_url, data=self.data)
        assert response.status_code == 404

    def test_check_user_wrong_id(self):
        """Реакция сервера на telegram_id, которого нет в базе"""
        data = {'telegram_id': 0}
        response = self.client.post(self.check_user_url, data=data)
        assert response.status_code == 404

    def test_check_user_correct_id(self):
        user = User.objects.create(**self.data)
        data = {'telegram_id': self.data['telegram_id']}
        response = self.client.post(self.check_user_url, data=data)
        assert response.status_code == 200
