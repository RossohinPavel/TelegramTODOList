from .users import _get_user_or_404
from .config import BaseSession, AsyncSession
from .models import Task
from pydantic import BaseModel
from datetime import datetime
from fastapi import HTTPException
from typing import Annotated


class CreateTaskSchema(BaseModel):
    title: str
    description: str = ''
    actual_on: Annotated[datetime, 'Timestamps']
    finish_by: Annotated[datetime, 'Timestamps']


class UpdateTaskSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    actual_on: Annotated[datetime, 'Timestamps'] | None = None
    finish_by: Annotated[datetime, 'Timestamps'] | None = None


async def get_tasks_list(phone_number: str | None = None, telegram_id: int | None = None):
    """Получение списка задач"""
    async with BaseSession() as session:
        user = await _get_user_or_404(session, phone_number, telegram_id)
        await session.refresh(user, attribute_names=["tasks"])
        return user.tasks


async def get_task(task_id: int):
    """Получение информации по задаче по ее id"""
    async with BaseSession() as session:
        return await _get_task_or_404(session, task_id)


async def _get_task_or_404(session: AsyncSession, task_id) -> Task:
    """Получение задачки или 404"""
    task = await session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail='Task not found')
    return task


async def create_task(data: CreateTaskSchema, phone_number: str | None = None, telegram_id: int | None = None):
    """Создание задачи"""
    async with BaseSession() as session:
        user = await _get_user_or_404(session, phone_number, telegram_id)
        task = await _update_task(Task(), user=user, **data.model_dump())
        session.add(task)
        try:
            await session.commit()
            return {'task': task.id}
        except:
            await session.rollback()


async def update_task(task_id: int, data: UpdateTaskSchema):
    """Обновление задачки"""
    async with BaseSession() as session:
        task = await _get_task_or_404(session, task_id)
        task = await _update_task(task, **data.model_dump())
        try:
            await session.commit()
        except:
            await session.rollback()


async def _update_task(task: Task, **kwargs):
    """Обновляет объект задачи и райзит ошибки, например, валидации"""
    try:
        for key, value in kwargs.items():
            if value is not None:
                setattr(task, key, value)
        return task
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=(str(ve)))


async def delete_task(task_id: int):
    """Удаление задачки"""
    async with BaseSession() as session:
        task = await _get_task_or_404(session, task_id)
        await session.delete(task)
        try:
            await session.commit()
        except:
            await session.rollback()
            raise HTTPException(status_code=500, detail='delete_task error')
