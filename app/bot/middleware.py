from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class CallbackExceptionHablerMiddleware(BaseMiddleware):
    """Обработчик возможных ошибок в каллбаках"""
    
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject, data: Dict[str, Any]) -> Any:
        try:
            return await handler(event, data)
        except Exception as e:
            await event.message.answer(text=str(e))
