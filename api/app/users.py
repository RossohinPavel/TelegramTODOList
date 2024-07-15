"""
Приложение для работы с пользователями. 
"""
from .sqla_config import BaseSession
from .models import User
from . import service


# async def check_user(params=Depends(UserSchema), session=Depends(get_session)):
#     """Проверка существования пользователя"""
#     return await _get_user_or_404(params, session)  


# async def _get_user_or_404(params: _BaseUserSchema, session: AsyncSession) -> User:
#     """Возвращает объект пользователя, если он сеть в базе или райзит 404"""
#     user = await _get_user(params, session)
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found") 
#     return user


# async def _get_user(params: _BaseUserSchema, session: AsyncSession) -> User | None:
#     """возвращает объект пользователя если он есть в базе или None"""
#     query = await service.get_query_user(params)
#     results = await session.execute(query)
#     return results.scalars().first()


async def get_user_id(phone_number: str | None = None, telegram_id: str | None = None) -> int:
    """Получение ид пользователя из базы данных"""
    async with BaseSession() as session:
        query = await service.get_query_user_id(telegram_id=telegram_id, phone_number=phone_number)
        results = await session.execute(query)
        return results.scalars().first()


async def create_user(phone_number: str = '', telegram_id: int | None = None):
    """Создание пользователя по номеру телефона"""
    if not phone_number:
        raise ValueError('phone_number should be defined')
    user = User(phone_number=phone_number, telegram_id=telegram_id)
    async with BaseSession() as session:
        session.add(user)
        try:
            await session.commit()
            await session.refresh(user)
            return {k: v for k, v in user.__dict__.items() if not k.startswith('_sa_')}
        except Exception as e:
            await session.rollback()
            raise e


# async def delete_user(user_id: int, session=Depends(get_session)):
#     """Удаление пользователя"""
#     user = await _get_user_or_404(UpdateUserSchema(id=user_id), session)
#     await session.delete(user)
#     try:
#         await session.commit()
#     except:
#         await session.rollback()
#         raise HTTPException(status_code=500, detail='delete_user error')


# async def update_user(user_id: int, data: UserSchema, session=Depends(get_session)):
#     """Обновление информации о пользователе"""
#     user = await _get_user_or_404(UpdateUserSchema(id=user_id), session)
#     if data.phone_number:
#         user.phone_number = data.phone_number
#     if data.telegram_id is not None:
#         user.telegram_id = data.telegram_id
#     try:
#         await session.commit()
#     except:
#         await session.rollback()
#         raise HTTPException(status_code=500, detail='update_user error')
