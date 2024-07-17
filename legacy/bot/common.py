"""Набор скриптов, которые отрабатывают для всего и вся"""
from aiogram import Router, types
from aiogram.filters.command import Command


common_router = Router(name='__common__')


MSG = "Бот находится в разработке. Многие функции могут быть переделаны."


@common_router.message(Command('help'))
async def cmd_help(message: types.Message):
    await message.answer(MSG)


@common_router.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(MSG)
