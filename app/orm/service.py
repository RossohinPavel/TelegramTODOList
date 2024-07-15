"""Содержит в себе скрипты запросов в sqlalchemy"""
from orm.models import User
from orm.config import BaseSession, AsyncSession
from functools import wraps
from sqlalchemy.exc import IntegrityError


def _session_decorator(func):
    """Декоратор для выдачи сессий на функции"""
    @wraps(func)
    async def inner(*args, **kwargs):
        async with BaseSession() as session:
            return await func(*args, session=session, **kwargs)
    return inner


@_session_decorator
async def get_user(telegram_id: int, session: AsyncSession = None):
    """Выдает объект пользователя"""
    return await session.get(User, telegram_id)


@_session_decorator
async def create_user(telegram_id: int, session: AsyncSession = None, **kwargs) -> User:
    """Создает пользователя по переданному telegram_id
       В kwargs можно дополнительно передать first_name, second_name, phone_number
    """
    try:
        user = User(id=telegram_id)
        for key, value in kwargs.items():
            setattr(user, key, value)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    except IntegrityError:
        await session.rollback()
        return 'User alredy exist'
    except Exception as e:
        await session.rollback()
        return f'User creation error {str(e)}'
