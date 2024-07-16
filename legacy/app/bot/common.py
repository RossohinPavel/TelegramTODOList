"""Набор скриптов, которые отрабатывают для всего и вся"""
from aiogram import Router, types
from aiogram.filters.command import Command


common_router = Router(name='__common__')


@common_router.message(Command('help'))
async def cmd_help(message: types.Message):
    msg = """Помощь!"""
    await message.answer(msg)
