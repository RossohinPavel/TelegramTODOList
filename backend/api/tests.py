from rest_framework.test import APITestCase

# Create your tests here.
class CheckUserTestCase(APITestCase):

    def test_send_wrong_number(self):
        """Тест реакции api на номер, которого нет в базе"""
        