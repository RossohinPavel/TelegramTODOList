"""Набор скриптов для генерации клавиатур"""
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def create_task_keyboard(id: int) -> InlineKeyboardBuilder:
    """Формирует клавиатуру для задачи"""
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Изменить', callback_data=f'edit:{id}')
    keyboard.button(text='Выполнить', callback_data=f'exec:{id}')
    keyboard.adjust(1)
    return keyboard.as_markup()
