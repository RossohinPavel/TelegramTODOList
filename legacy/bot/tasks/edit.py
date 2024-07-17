"""Набор скриптов по редактированию и выполнению задачи"""
from aiogram import Router, types, F
from orm import service
from .list import back_to_list


edit_router = Router(name='__edit__')


@edit_router.callback_query(F.data.startswith('exec'))
async def execute_task(callback_query: types.CallbackQuery):
    """Выполнение задачи"""
    await service.execute_task(int(callback_query.data[5:]))
    await callback_query.answer(text='Задача выполнена')
    await back_to_list(callback_query)
