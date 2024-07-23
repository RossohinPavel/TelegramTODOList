"""Набор скриптов для генерации клавиатур"""
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup


async def create_task_keyboard() -> InlineKeyboardMarkup:
    """Формирует клавиатуру для задачи"""
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Изменить', callback_data=f'edit')
    keyboard.button(text='Выполнить', callback_data=f'exec')
    keyboard.adjust(2)
    return keyboard.as_markup()


async def create_task_edit_keyboard() -> InlineKeyboardMarkup:
    """Генерация клавиатуры для редактирования задачи"""
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Название', callback_data=f'title')
    keyboard.button(text='Описание', callback_data=f'desc')
    keyboard.button(text='Отмена', callback_data=f'back')
    keyboard.button(text='Сохранить', callback_data=f'save')
    keyboard.adjust(2)
    return keyboard.as_markup()
