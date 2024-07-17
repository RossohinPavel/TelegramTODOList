"""Набор скриптов для генерации клавиатур"""
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup


async def create_task_keyboard(id: int) -> InlineKeyboardMarkup:
    """Формирует клавиатуру для задачи"""
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Изменить', callback_data=f'edit:{id}')
    keyboard.button(text='Выполнить', callback_data=f'exec:{id}')
    keyboard.adjust(2)
    return keyboard.as_markup()


async def create_task_edit_keyboard() -> InlineKeyboardMarkup:
    """Генерация клавиатуры для редактирования задачи"""
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Название', callback_data=f'name')
    keyboard.button(text='Описание', callback_data=f'desc')
    keyboard.button(text='Назад', callback_data=f'back')
    keyboard.button(text='Сохранить', callback_data=f'save')
    keyboard.adjust(2)
    return keyboard.as_markup()