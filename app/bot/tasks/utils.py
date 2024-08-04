"""Набор утилит для работы с задачами"""
from aiogram import types, Bot


async def reduce_task_content(text: str) -> str:
    """Сокращает тест задачи до 15 символов"""
    if len(text) > 12:
        text = text[:12] + '...'
    return text


async def get_file_binary(bot: Bot, file_info: str):
    """Возвращает бинарный объект файла"""
    file = await bot.get_file(file_info)
    return await bot.download_file(file.file_path)
