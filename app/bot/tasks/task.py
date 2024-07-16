from aiogram import Router, types, F
from orm import service
from . import utils, keyboards

task_router = Router(name='__task__')


@task_router.callback_query(F.data.startswith('task'))
async def get_task(callback_query: types.CallbackQuery):
    """Получение информации по одной задаче"""
    task = await service.get_task(int(callback_query.data[5:]))
    text = await utils.get_tasks_text(task)
    keyboard = await keyboards.create_task_keyboard(task.id)
    await callback_query.message.edit_text(text=text, reply_markup=keyboard)
