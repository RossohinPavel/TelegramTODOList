"""Содержит в себе скрипты запросов в sqlalchemy"""
from orm.config import BaseSession, AsyncSession
from sqlalchemy import select, update
from functools import wraps
from orm.models import Task


def _session_decorator(func):
    """Декоратор для выдачи сессий на функции"""
    @wraps(func)
    async def inner(*args, **kwargs):
        async with BaseSession() as session:
            return await func(*args, session=session, **kwargs)
    return inner


@_session_decorator
async def create_task(telegram_id: int, title: str, session: AsyncSession = None) -> int:
    """Создание задачи. Возвращает ее id"""
    try:
        task = Task(telegram_id=telegram_id, title=title)
        session.add(task)
        await session.commit()
        return task.id
    except Exception as e:
        await session.rollback()
        return str(e)


@_session_decorator
async def get_tasks_list(telegram_id: int, session: AsyncSession = None):
    """Выдает список задач пользователя в виде генератора"""
    query = (
        select(Task.id, Task.title, Task.status).
        where(Task.telegram_id == telegram_id, Task.executed == False)
    )
    return await session.execute(query)
     


@_session_decorator
async def get_task(id: int, session: AsyncSession = None):
    """Выдает задачу"""
    return await session.get(Task, id)


@_session_decorator
async def execute_task(id: int, session: AsyncSession = None):
    """Выполняет задачу"""
    query = (
        update(Task).
        where(Task.id == id).
        values(executed=True)
    )
    try: 
        await session.execute(query)
        await session.commit()
        return True
    except Exception as e:
        return str(e)
