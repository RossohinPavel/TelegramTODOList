from pydantic import BaseModel
from fastapi import HTTPException
from typing import Annotated, Any
from datetime import datetime


class _BaseUserSchema(BaseModel):
    """Базовая схема для пользователя"""


class UserSchema(_BaseUserSchema):
    phone_number: str | None = None
    telegram_id: int | None = None

    def model_post_init(self, __context) -> None:
        """Метод для проверки, чтобы один из атрибутов был со значением != None"""
        if all(map(lambda x: x is None, self.__dict__.values())):
            raise HTTPException(status_code=400)


class CreateUserSchema(_BaseUserSchema):
    phone_number: str
    telegram_id: int | None = None


class UpdateUserSchema(_BaseUserSchema):
    id: int


class CreateTaskSchema(BaseModel):
    title: str
    description: str | None = None
    actual_on: Annotated[datetime, 'Timestamps']
    finish_by: Annotated[datetime, 'Timestamps']


class UpdateTaskSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    actual_on: Annotated[datetime, 'Timestamps'] | None = None
    finish_by: Annotated[datetime, 'Timestamps'] | None = None
    executed: bool | None = None
