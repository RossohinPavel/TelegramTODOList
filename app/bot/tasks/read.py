"""Скрипты для организации просмотра списка и одиночной задачи"""
from aiogram import Router, types
from aiogram.filters.command import Command
from orm import service
from bot.tasks import keyboards, utils


read_router = Router(name='__read__')


LIST_TITLE = 'Актуальные задачи:'


@read_router.message(Command('list'))
async def get_tasks_list(message: types.Message):
    """Отдает список задачек пользователя"""
    keyboard = await _get_tasks_keyboard(message.from_user.id)
    await message.answer(text=LIST_TITLE, reply_markup=keyboard)


async def _get_tasks_keyboard(telegram_id: int):
    """Возвращает сгенерированную клавиатуру для задач"""
    res = await service.get_tasks_list(telegram_id=telegram_id)
    keyboard = await keyboards.create_list_keyboard(res)
    return keyboard


@read_router.callback_query(lambda c: c.data and c.data.startswith('id'))
async def get_task(callback_query: types.CallbackQuery):
    """Получение информации по одной задаче"""
    task = await service.get_task(int(callback_query.data[3:]))
    text = await _get_tasks_text(task)
    keyboard = await keyboards.create_task_keyboard(task.id)
    await callback_query.message.edit_text(text=text, reply_markup=keyboard)


@read_router.callback_query(lambda c: c.data and c.data.startswith('back'))
async def back_to_list(callback_query: types.CallbackQuery):
    """Возвращение к списку задач"""
    keyboard = await _get_tasks_keyboard(callback_query.from_user.id)
    await callback_query.message.edit_text(text=LIST_TITLE, reply_markup=keyboard)


async def _get_tasks_text(task: service.Task):
    """Форматирует текст задачи"""
    text = await utils.create_task_name({'title': task.title, 'status': task.status})
    text += '\n'
    if task.description:
        text += task.description + '\n'
    text += 'Актуально с ' + str(task.actual_on) + '\n'
    text += 'Выполнить к ' + str(task.finish_by)
    return text
