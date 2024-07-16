"""Набор скриптов по редактированию и выполнению задачи"""
from aiogram import Router, types
from orm import service
# from .read import back_to_list


edit_router = Router(name='__edit__')


# @edit_router.callback_query(lambda c: c.data and c.data.startswith('exec'))
# async def execute_task(callback_query: types.CallbackQuery):
#     """Выполнение задачи"""
#     await service.execute_task(int(callback_query.data[5:]))
#     await callback_query.message.edit_reply_markup(reply_markup=None)
#     await back_to_list(callback_query)
