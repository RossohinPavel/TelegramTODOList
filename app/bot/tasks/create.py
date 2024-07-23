"""Набор скриптов для работы с созданием задачи"""
from aiogram import Router, types, F
from orm import service
from . import keyboards as kb


create_router = Router(name='__create_task__')


@create_router.message(F.content_type.in_({'text'}))
async def init_create_task(message: types.Message):
    """Инициализация создания задачи по текстовому вводу пользователя"""
    await message.delete()
    task_message = await message.answer(message.text, reply_markup=kb.TASK_KEYBOARD)
    task = await service.create_task(task_message.chat.id, task_message.message_id, task_message.text)
    if isinstance(task, str):
        task_message.delete()
        await message.answer(text=task)
