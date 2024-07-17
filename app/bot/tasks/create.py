"""Набор скриптов для работы с созданием задачи"""
from aiogram import Router, types, F
from orm import service, models
from . import utils
from . import keyboards


create_router = Router(name='__create_task__')


@create_router.message(F.content_type.in_({'text'}))
async def init_create_task(message: types.Message):
    """Инициализация создания задачи по текстовому вводу пользователя"""
    title, desc = await utils.parse_message_text(message.text)
    task = await service.create_task(message.from_user.id, title, desc)
    if isinstance(task, str):
        await message.answer(text=task)
    else:
        await show_task_entity(message, task)
    await message.delete()


async def show_task_entity(message: types.Message, task: models.Task):
    """Показывает задачу"""
    text = await utils.create_task_text(task)
    kb = await keyboards.create_task_keyboard(task.id)
    msg = await message.answer(text=text)
    await msg.edit_reply_markup(reply_markup=kb)
