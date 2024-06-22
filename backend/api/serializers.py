from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def validate_work_time(self, value):
        print(f'  --  {value}  --  ', type(value))
        return value
