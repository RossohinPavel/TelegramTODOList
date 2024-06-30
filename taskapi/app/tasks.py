from .users import _get_user_or_404
from .config import BaseSession, AsyncSession
from .models import Task
from pydantic import BaseModel


class CreateTaskSchema(BaseModel):
    title: str
    description: str = ''


async def get_tasks_list():
    pass


async def get_task():
    pass


async def create_task(phone_number: str | None = None, telegram_id: int | None = None):
    """Создание задачи"""
    async with BaseSession() as session:
        user = await _get_user_or_404(session, phone_number, telegram_id)


async def update_task():
    pass


async def delete_task():
    pass
