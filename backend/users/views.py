from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view

from .models import User


def _get_response_dct(message, status: str = 'ok'):
    """Возвращает заготовленный словарь для ответа сервера."""
    return {'status': status, 'message': message}


@api_view(['POST'])
def set_telegram_id(request: Request):
    """Добавление telegram_id пользователю"""
    phone = request.data.get('phone', None)
    telegram_id = request.data.get('telegram_id', None)
    user = get_object_or_404(User, phone=phone)
    user.telegram_id = telegram_id
    user.save()
    return Response(_get_response_dct(f'Аккаунт подключен для пользователя {user.username}'))


@api_view(['POST'])
def check_user(request: Request):
    """Проверка подключения телеграм id"""
    telegram_id = request.data.get('telegram_id', None)
    user = get_object_or_404(User, telegram_id=telegram_id)
    return Response(_get_response_dct(f'Добро пожаловать {user.username}!'))
