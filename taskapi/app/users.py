"""
Приложение для работы с пользователями. 
Публичные функции - обработчики запроса. 
Защищенные - выполняют работу с базой данных
"""
from sqlalchemy import select
from fastapi import HTTPException, Depends
from .config import AsyncSession, get_session
from .models import User
from .schemas import _BaseUserSchema, UserSchema, CreateUserSchema, UpdateUserSchema


async def check_user(params=Depends(UserSchema), session=Depends(get_session)):
    """Проверка существования пользователя"""
    return await _get_user_or_404(params, session)  


async def _get_user_or_404(params: _BaseUserSchema, session: AsyncSession) -> User:
    """Возвращает объект пользователя, если он сеть в базе или райзит 404"""
    user = await _get_user(params, session)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found") 
    return user


async def _get_user(params: _BaseUserSchema, session: AsyncSession) -> User | None:
    """возвращает объект пользователя если он есть в базе или None"""
    query = select(User)
    for key, value in params.__dict__.items():
        if value is not None:
            query = query.where(eval(f'User.{key} == params.{key}'))
            break
    results = await session.execute(query)
    return results.scalars().first()


async def create_user(params: CreateUserSchema, session=Depends(get_session)):
    """Создание пользователя по номеру телефона"""
    user = await _get_user(params, session)
    if user is not None:
        raise HTTPException(status_code=422, detail='User alredy existing')
    # Создание пользователя
    user = await _create_user(params, session)
    await session.refresh(user)
    return user


async def _create_user(params: CreateUserSchema, session: AsyncSession) -> User | None:
    """Создает пользователя и возвращает его id"""
    # Проверяем наличие пользователя в базе
    user = User(phone_number=params.phone_number)
    session.add(user)
    try:
        await session.commit()
        return user
    except:
        await session.rollback()
        raise HTTPException(status_code=500, detail='create_user error')


async def delete_user(user_id: int, session=Depends(get_session)):
    """Удаление пользователя"""
    user = await _get_user_or_404(UpdateUserSchema(id=user_id), session)
    await session.delete(user)
    try:
        await session.commit()
    except:
        await session.rollback()
        raise HTTPException(status_code=500, detail='delete_user error')


async def update_user(user_id: int, data: UserSchema, session=Depends(get_session)):
    """Обновление информации о пользователе"""
    user = await _get_user_or_404(UpdateUserSchema(id=user_id), session)
    if data.phone_number:
        user.phone_number = data.phone_number
    if data.telegram_id is not None:
        user.telegram_id = data.telegram_id
    try:
        await session.commit()
    except:
        await session.rollback()
        raise HTTPException(status_code=500, detail='update_user error')
