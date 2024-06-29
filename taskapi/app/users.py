from pydantic import BaseModel
from sqlalchemy import select
from .config import BaseSession, AsyncSession
from .models import User


class UserSchema(BaseModel):
    """Валидация значений для создания пользоваетля"""
    phone_number: str
    telegram_id: int | None = None


# Функции для приложения FastApi
async def check_user(phone_number: str | None = None, telegram_id: int | None = None):
    """Проверка существования пользователя"""
    async with BaseSession() as session:
        user = await _check_user(session, phone_number, telegram_id)
    response = {"message": "user does not exist"}
    if user is not None:
        response['message'] = f'user id={user[0].id}'
    return response


async def create_user(user: UserSchema):
    """Создание пользователя по номеру телефона"""
    async with BaseSession() as session:
        user = await _create_user(session, user.phone_number, user.telegram_id)
    
    response = {'message': 'exception inside create_user'}
    if user:
        response['message'] = f'created user from id {user.id}'
    return response


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


async def _create_user(session: AsyncSession, phone_number: str, telegram_id: int | None = None) -> User | None:
    """Создает пользователя и возвращает его id"""
    # Проверяем наличие пользователя в базе
    user = await _check_user(session, phone_number, telegram_id)
    # Если его нет - создаем
    if user is None:
        user = User(phone_number=phone_number, telegram_id=telegram_id)
        session.add(user)
    else:
        user = user[0]
    # Прицепялем telegram_id если такого нет
    if user.telegram_id is None and telegram_id is not None:
        user.telegram_id = telegram_id
    try:
        await session.commit()
        return user
    except:
        await session.rollback()
