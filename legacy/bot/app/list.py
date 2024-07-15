"""Скрипт для отрисовки клавиатуры управления задачами"""
from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiohttp import ClientSession
from . import config


list_router = Router(name='__list__')


@list_router.message(Command('list'))
async def cmd_list(message: types.Message):
    """Формирует список задач и вывод их в виде клавиатуры"""
    data = await get_tasks_list(message.from_user.id)
    keyboard = await create_keyboard(data)
    await message.answer(text='Ваши задачи:', reply_markup=keyboard)


async def get_tasks_list(telegram_id: int) -> list[dict]:
    """Получает от api список задач"""
    async with ClientSession() as session:
        async with session.get(config.API_ROOT_URL, params={'telegram_id': telegram_id}) as resp:
            return await resp.json()


async def create_keyboard(tasks: list[dict]):
    """Создает клавиатуру по списку задач"""
    keyboard = InlineKeyboardBuilder()
    for task in tasks:
        text = await _get_task_name(task)
        keyboard.button(text=text, callback_data=f'id:{task['id']}')
    keyboard.button(text='_Обновить_', callback_data='update:')
    keyboard.adjust(1)
    return keyboard.as_markup()


async def _get_task_name(task: dict) -> str:
    """Формирует имя задачи для отображения в списке"""
    # Формируем кружок, обозначающий статус задачи
    match task['status']:
        case 2: circle = config.RED_CIRCLE
        case 1: circle = config.YELLOW_CIRCLE
        case 0 | _: circle = config.WHITE_CIRCLE
    # Обрезаем имя задачи, если оно слишком длинное
    title = task['title']
    if len(title) > 22:
        title = title[:19] + '...'
    return f'{circle} {title}'
