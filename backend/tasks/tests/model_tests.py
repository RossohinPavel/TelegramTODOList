from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from tasks.models import Task
from users.models import User
from django.core.exceptions import ValidationError

# Create your tests here.
class ModelTestCase(TestCase):

    def setUp(self) -> None:
        now = timezone.now()
        self.task = Task(
            user=User.objects.create(),
            title='test',
            description='test',
            actual_on=now,
            finish_by= now
        )

    def test_validation(self):
        """Тест валидации модели"""
        # Не даст сохранить модель, когда finish_by равно actual_on
        with self.assertRaises(ValidationError):
            self.task.save()
        # Или меньше
        self.task.finish_by = self.task.finish_by - timedelta(hours=1)
        with self.assertRaises(ValidationError):
            self.task.save()

    def test_status_0(self):
        """Тест статуса - выполнен"""
        time = self.task.finish_by + timedelta(hours=1)
        self.task.finish_by = time
        self.task.excuted_on = time
        self.task.save()
        assert Task.objects.get(pk=self.task.pk).status == 0

    def test_status_1(self):
        """Тест статуса 1 - в очереди"""
        time = self.task.actual_on
        self.task.actual_on = time + timedelta(hours=1)
        self.task.finish_by = time + timedelta(hours=2)
        self.task.save()
        assert Task.objects.get(pk=self.task.pk).status == 1

    def test_status_2(self):
        """Тест статуса 2 - актуально"""
        time = self.task.actual_on
        self.task.actual_on = time - timedelta(hours=1)
        self.task.finish_by = time + timedelta(hours=1)
        self.task.save()
        assert Task.objects.get(pk=self.task.pk).status == 2

    def test_status_3(self):
        """Тест статуса 3 - просрочено"""
        time = self.task.actual_on
        self.task.actual_on = time - timedelta(hours=2)
        self.task.finish_by = time - timedelta(hours=1)
        self.task.save()
        assert Task.objects.get(pk=self.task.pk).status == 3
