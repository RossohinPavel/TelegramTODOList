"""Содержит в себе скрипты запросов в sqlalchemy"""
from sqlalchemy import delete, update
from orm.config import BaseSession, AsyncSession
from functools import wraps
from orm.models import Task


def _session_decorator(func):
    """Декоратор для выдачи сессий на функции"""
    @wraps(func)
    async def inner(*args, **kwargs):
        async with BaseSession() as session:
            try:
                return await func(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()
                return str(e)
    return inner


@_session_decorator
async def create_task(telegram_id: int, title: str, description: str | None, session: AsyncSession = None) -> int:
    """Создание задачи. Возвращает ее id"""
    task = Task(telegram_id=telegram_id, title=title, description=description)
    session.add(task)
    await session.commit()
    return task


@_session_decorator
async def update_task(id: int, title: str, description: str | None, session: AsyncSession = None):
    """Выдает список задач пользователя в виде генератора"""
    if isinstance(id, str):
        id = int(id)
    stmt = (
        update(Task).
        where(Task.id == id).
        values(title=title, description=description)
    )
    await session.execute(stmt)
    await session.commit()
    return True


@_session_decorator
async def execute_task(id: int | str, session: AsyncSession = None):
    """Выполняет задачу"""
    if isinstance(id, str):
        id = int(id)
    stmt = (
        delete(Task).
        where(Task.id == id)
    )
    await session.execute(stmt)
    await session.commit()
    return True
