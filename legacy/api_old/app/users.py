"""
Приложение для работы с пользователями. 
Публичные функции - обработчики запроса. 
Защищенные - выполняют работу с базой данных
"""
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, HTTPException, Depends
from .config import AsyncSession, get_session
from .models import User
from .schemas import _BaseUserSchema, UserSchema, CreateUserSchema, UpdateUserSchema
from . import service


users_router = APIRouter(prefix='/users')


@users_router.get("")
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
    query = await service.get_query_user(params)
    results = await session.execute(query)
    return results.scalars().first()


@users_router.post("", status_code=201)
async def create_user(params: CreateUserSchema, session=Depends(get_session)):
    """Создание пользователя по номеру телефона"""
    user = User(**params.model_dump(exclude_none=True))
    session.add(user)
    try:
        await session.commit()
        await session.refresh(user)
        return user
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=422, detail='User alredy existing')
    except:
        await session.rollback()
        raise HTTPException(status_code=500, detail='create_user error')


@users_router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, session=Depends(get_session)):
    """Удаление пользователя"""
    user = await _get_user_or_404(UpdateUserSchema(id=user_id), session)
    await session.delete(user)
    try:
        await session.commit()
    except:
        await session.rollback()
        raise HTTPException(status_code=500, detail='delete_user error')


@users_router.patch("/{user_id}", status_code=200)
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
