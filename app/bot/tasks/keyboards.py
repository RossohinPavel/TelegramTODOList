"""Набор скриптов для генерации клавиатур"""
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton


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
    # keyboard.button(text='Подзадача', callback_data=f'sub')
    keyboard.button(text='Содержание', callback_data=f'content')
    keyboard.adjust(1)
    keyboard.row(
        InlineKeyboardButton(text='Отмена', callback_data='back'),
        InlineKeyboardButton(text='Сохранить', callback_data=f'save'),
        width=2
    )
    return keyboard.as_markup()
