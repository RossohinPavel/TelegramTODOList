"""Набор скриптов для редактирования задачи"""
from aiogram import Router, types
from orm import service


update_router = Router(name='__update__')


@update_router.callback_query(lambda c: c.data and c.data.startswith('exec:'))
async def execute_task(callback_query: types.CallbackQuery):
    """Ловит калбэк с клавиатуры и выполняет задачу"""
    task_id = callback_query.data[5:]
    if not task_id.isdigit():
        return
    await callback_query.message.delete()
    task_name, *_ = callback_query.message.text.split('\n', maxsplit=1)
    await callback_query.answer(text=f'Задача <{task_name}> выполнена.')
    await service.execute_task(int(task_id))
