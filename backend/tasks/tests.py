from django.test import TestCase
from django.utils import timezone
from .models import Task
from users.models import User
from django.core.exceptions import ValidationError

# Create your tests here.
class ModelTestCase(TestCase):

    def test_validation(self):
        """Тест валидации модели"""
        now = timezone.now()
        user = User.objects.create()
        t = Task(
            user=user,
            title='test',
            description='test',
            actual_on=now,
            finish_by=now
        )
        with self.assertRaises(ValidationError):
            t.save()
