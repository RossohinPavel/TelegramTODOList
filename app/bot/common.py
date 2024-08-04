"""Набор скриптов, которые отрабатывают для всего и вся"""
from aiogram import Router, types
from aiogram.filters.command import Command


common_router = Router(name='__common__')


START_MSG = "Бот находится в разработке. Многие функции могут быть переделаны."
HELP_MSG = """Для создания задачи просто отправьте текстовое сообщение боту. Также можно отправить голосовое сообщение."""


@common_router.message(Command('help'))
async def cmd_help(message: types.Message):
    await message.answer(HELP_MSG)


@common_router.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(START_MSG + '\n' + HELP_MSG)
