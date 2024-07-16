"""Набор скриптов для генерации клавиатур"""
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from typing import Iterable
from bot.tasks import utils
from orm.models import Task


async def create_list_keyboard(tasks_list: Iterable[Task]) -> InlineKeyboardMarkup:
    """Создает клавиатуру по списку задач"""
    keyboard = InlineKeyboardBuilder()
    for task in tasks_list:
        text = await utils.create_task_name(task)
        keyboard.button(text=text, callback_data=f'id:{task.id}')
    keyboard.adjust(1)
    return keyboard.as_markup()


async def create_task_keyboard(id: int) -> InlineKeyboardMarkup:
    """Формирует клавиатуру для задачи"""
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Изменить', callback_data='edit')
    keyboard.button(text='Выполнить', callback_data='execute')
    keyboard.button(text='Назад', callback_data='back')
    keyboard.adjust(2)
    return keyboard.as_markup()
