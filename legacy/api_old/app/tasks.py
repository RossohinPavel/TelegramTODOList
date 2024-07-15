"""
Приложение для работы с задачами.
"""
from fastapi import APIRouter, Depends, HTTPException
from .config import AsyncSession, get_session
from .schemas import UserSchema, CreateTaskSchema, UpdateTaskSchema
from .users import _get_user_or_404
from .models import Task
from . import service


tasks_router = APIRouter(prefix='')


@tasks_router.get('/')
async def get_tasks_list(params=Depends(UserSchema), session=Depends(get_session)):
    """Получение списка задач"""
    results = await session.execute(await service.get_query_tasks_list(params))
    return [row._mapping for row in results]


@tasks_router.get('/{task_id}')
async def get_task(task_id: int, session=Depends(get_session)):
    """Получение информации по задаче по ее id"""
    return await _get_task_or_404(task_id, session)


async def _get_task_or_404(task_id: int, session: AsyncSession) -> Task:
    """Получение задачки или 404"""
    task = await session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail='Task not found')
    return task


@tasks_router.post('/', status_code=201)
async def create_task(data: CreateTaskSchema, params=Depends(UserSchema), session=Depends(get_session)):
    """Создание задачи"""
    task = await _update_task(Task(), **data.model_dump(exclude_none=True))
    task.user = await _get_user_or_404(params, session)
    session.add(task)
    try:
        await session.commit()
        await session.refresh(task)
        return task
    except:
        await session.rollback()
        raise HTTPException(status_code=500, detail='create_task error')


@tasks_router.patch('/{task_id}', status_code=200)
async def update_task(task_id: int, data: UpdateTaskSchema, session=Depends(get_session)):
    """Обновление задачки"""
    task = await _get_task_or_404(task_id, session)
    task = await _update_task(task, **data.model_dump(exclude_none=True))
    try:
        await session.commit()
    except:
        await session.rollback()


async def _update_task(task: Task, **kwargs) -> Task:
    """Обновляет объект задачи и райзит ошибки, например, валидации"""
    try:
        for key, value in kwargs.items():
            setattr(task, key, value)
        return task
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=(str(ve)))


@tasks_router.delete('/{task_id}', status_code=204)
async def delete_task(task_id: int, session=Depends(get_session)):
    """Удаление задачки"""
    task = await _get_task_or_404(task_id, session)
    await session.delete(task)
    try:
        await session.commit()
    except:
        await session.rollback()
        raise HTTPException(status_code=500, detail='delete_task error')
