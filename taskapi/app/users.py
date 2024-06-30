"""
Приложение для работы с пользователями. 
Публичные функции - обработчики запроса. 
Защищенные - выполняют работу с базой данных
"""
from pydantic import BaseModel
from sqlalchemy import select
from fastapi import HTTPException
from .config import BaseSession, AsyncSession
from .models import User


class CreateUserSchema(BaseModel):
    phone_number: str
    telegram_id: int | None = None


class UpdateUserSchema(BaseModel):
    phone_number: str | None = None
    telegram_id: int | None = None


async def check_user(phone_number: str | None = None, telegram_id: int | None = None):
    """Проверка существования пользователя"""
    if phone_number is None and telegram_id is None:
        raise HTTPException(status_code=400)

    async with BaseSession() as session:
        user = await _check_user(session, phone_number, telegram_id)
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user[0]


async def _check_user(session: AsyncSession, phone_number: str | None = None, telegram_id: int | None = None) -> User | None:
    """возвращает объект пользователя если он есть в базе"""
    query = None
    if telegram_id is not None:
        query = User.telegram_id == telegram_id
    if phone_number is not None:
        query = User.phone_number == phone_number

    if query is not None:
        res = await session.execute(select(User).where(query))
        return res.first()


async def create_user(data: CreateUserSchema):
    """Создание пользователя по номеру телефона"""
    async with BaseSession() as session:
        user = await _check_user(session, data.phone_number, data.telegram_id)
        if user is not None:
            raise HTTPException(status_code=422, detail='User alredy existing')
        # Создание пользователя
        user = await _create_user(session, data.phone_number, data.telegram_id)
    
    return user


async def _create_user(session: AsyncSession, phone_number: str, telegram_id: int | None = None) -> User | None:
    """Создает пользователя и возвращает его id"""
    # Проверяем наличие пользователя в базе
    user = User(phone_number=phone_number, telegram_id=telegram_id)
    session.add(user)
    try:
        await session.commit()
        return user
    except:
        await session.rollback()


async def delete_user(user_id: int):
    """Удаление пользователя"""
    async with BaseSession() as session:
        user = await _get_user_from_id(session, user_id)
        await session.delete(user)
        try:
            await session.commit()
        except:
            await session.rollback()
            raise HTTPException(status_code=500, detail='Something went wrong')


async def _get_user_from_id(session: AsyncSession, user_id) -> User:
    """Возвращает объект пользователя или райзит 404"""
    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def update_user(user_id: int, data: UpdateUserSchema):
    """Обновление информации о пользователе"""
    if data.phone_number is None and data.telegram_id is None:
        raise HTTPException(status_code=400)
    async with BaseSession() as session:
        user = await _get_user_from_id(session, user_id)
        if data.phone_number:
            user.phone_number = data.phone_number
        if data.telegram_id is not None:
            user.telegram_id = data.telegram_id
        try:
            await session.commit()
        except:
            await session.rollback()
            raise HTTPException(status_code=500, detail='Something went wrong')
