"""Набор скриптов для генерации клавиатур"""
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.tasks import utils
from orm.models import Task


async def create_list_keyboard(tasks: list[Task]) -> InlineKeyboardBuilder:
    """Создает клавиатуру по списку задач"""
    keyboard = InlineKeyboardBuilder()
    keyboard.adjust(1)
    for task in tasks:
        text = await utils.create_task_name(task)
        keyboard.button(text=text, callback_data=f'task:{task.id}')
    return keyboard


async def update_empty_keyboard(keyboard: InlineKeyboardBuilder):
    """Обновляет пустую клавиатуру"""
    keyboard.button(text='Добавить задачу', callback_data='create')


async def create_task_keyboard(id: int) -> InlineKeyboardBuilder:
    """Формирует клавиатуру для задачи"""
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Изменить', callback_data='edit')
    keyboard.button(text='Выполнить', callback_data=f'exec:{id}')
    keyboard.button(text='Назад', callback_data='back')
    keyboard.adjust(2)
    return keyboard.as_markup()
