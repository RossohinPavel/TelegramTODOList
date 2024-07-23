"""Набор скриптов для работы с созданием задачи"""
from aiogram import Router, types, F
from orm import service, models
from . import utils
from . import keyboards


create_router = Router(name='__create_task__')


@create_router.message(F.content_type.in_({'text'}))
async def init_create_task(message: types.Message):
    """Инициализация создания задачи по текстовому вводу пользователя"""
    task = await service.create_task(message.from_user.id, message.message_id, message.text)
    if isinstance(task, str):
        await message.answer(text=task)
    else:
        await show_task_entity(message, task)
    await message.delete()


async def show_task_entity(message: types.Message, task: models.Task):
    """Показывает задачу"""
    text = task.content
    kb = await keyboards.create_task_keyboard()
    msg = await message.answer(text=text)
    await msg.edit_reply_markup(reply_markup=kb)
