from pydantic import BaseModel
from fastapi import HTTPException


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


class UpdateUserSchema(_BaseUserSchema):
    id: int
