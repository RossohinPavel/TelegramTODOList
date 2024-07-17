"""Скрипты для организации просмотра списка задач"""
from aiogram import Router, types, F
from aiogram.filters.command import Command
from bot.tasks import keyboards, utils
from orm import service


list_router = Router(name='__list__')


@list_router.message(Command('list'))
async def get_tasks_list(message: types.Message):
    """Отдает список задачек пользователя"""
    msg, keyboard = await _get_task_list_msg_content(message.from_user.id)
    await message.answer(text=msg, reply_markup=keyboard)


async def _get_task_list_msg_content(id: int):
    """Возвращает текст и клавиатуру для задачек."""
    tasks = await service.get_tasks_list(id)
    msg = utils.LIST_MSG
    keyboard = await keyboards.create_list_keyboard(tasks)
    if not keyboard._markup:
        msg = utils.EMPTY_LIST_MSG
        await keyboards.update_empty_keyboard(keyboard)
    return msg, keyboard.as_markup()


@list_router.callback_query(F.data == 'back')
async def back_to_list(callback_query: types.CallbackQuery):
    """Возвращение к списку задач"""
    msg, keyboard = await _get_task_list_msg_content(callback_query.from_user.id)
    await callback_query.message.edit_text(text=msg, reply_markup=keyboard)
