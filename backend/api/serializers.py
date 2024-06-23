from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    status = serializers.IntegerField(required=False)

    class Meta:
        model = Task
        fields = '__all__'


class TasksListSerializer(serializers.ModelSerializer):
    status = serializers.IntegerField(required=False)

    class Meta:
        model = Task
        fields = ['id', 'title', 'status']
