from rest_framework import serializers
from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    status = serializers.IntegerField()

    class Meta:
        model = Task
        exclude = ('user', )


class TasksListSerializer(serializers.ModelSerializer):
    status = serializers.IntegerField()

    class Meta:
        model = Task
        fields = ('id', 'title', 'status')
