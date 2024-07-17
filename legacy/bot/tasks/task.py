from aiogram import Router, types, F
from orm import service
from . import utils, keyboards

task_router = Router(name='__task__')


@task_router.callback_query(F.data.startswith('task'))
async def get_task(callback_query: types.CallbackQuery):
    """Получение информации по одной задаче"""
    text, keyboard = await _get_task_msg_content(int(callback_query.data[5:]))
    await callback_query.message.edit_text(text=text, reply_markup=keyboard)


async def _get_task_msg_content(id: int):
    """Отдает отформатированное сообщение по задаче и клавиатуру для нее"""
    task = await service.get_task(id)
    text = await utils.get_tasks_text(task)
    keyboard = await keyboards.create_task_keyboard(task.id)
    return text, keyboard.as_markup()