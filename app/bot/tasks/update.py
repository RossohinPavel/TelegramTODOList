"""Набор скриптов для редактирования задачи"""
from aiogram import Router, types, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from orm import service
from . import keyboards as kb
from . import utils


class TaskState(StatesGroup):
    edit = State()


update_router = Router(name='__update__')


@update_router.callback_query(lambda c: c.data and c.data.startswith('exec'))
async def execute_task(callback_query: types.CallbackQuery):
    """Ловит калбэк с клавиатуры и выполняет задачу"""
    await service.execute_task(callback_query.message.chat.id, callback_query.message.message_id)
    await callback_query.message.delete()
    task = await utils.reduce_task_content(callback_query.message.text)
    await callback_query.answer(text=f'Задача <{task}> выполнена.')


@update_router.callback_query(lambda c: c.data and c.data.startswith('edit'))
async def init_edit(callback_query: types.CallbackQuery, state: FSMContext):
    """Инициализация редактирования задачи"""
    await state.set_state(TaskState.edit)
    msg = await callback_query.message.edit_reply_markup(reply_markup=kb.EDIT_KEYBOARD)
    data = {'origin_text': msg.text, 'task_msg': msg, 'query_msg': None}
    await state.set_data(data)


@update_router.callback_query(TaskState.edit, F.data == 'back')
async def restore_task_content(callback_query: types.CallbackQuery, state: FSMContext):
    """Сбросить все изменения и восстановить текст задачи."""
    await _back_to_main_entity(callback_query, state)


@update_router.callback_query(TaskState.edit, F.data == 'save')
async def save_task_content(callback_query: types.CallbackQuery, state: FSMContext):
    """Сохранить изменения в задаче."""
    await _back_to_main_entity(callback_query, state, save=True)


async def _back_to_main_entity(callback_query: types.CallbackQuery, state: FSMContext, save=False):
    """Возвращает к основному сосотоянию задачи и сейвит текст по необходимости"""
    data = await state.get_data()
    await state.clear()
    if save:
        msg = data['task_msg']
        await service.update_task(msg.chat.id, msg.message_id, msg.text)
    else:
        await callback_query.message.edit_text(text=data['origin_text'])
    await callback_query.message.edit_reply_markup(reply_markup=kb.TASK_KEYBOARD)


@update_router.callback_query(TaskState.edit, F.data == 'content')
async def init_task_title_edit(callback_query: types.CallbackQuery, state: FSMContext):
    """Инициализация редактирования задачи"""
    text = 'Введите новый текст задачи.\nЕсли нужно поменять текст в сторой задаче - скопируйте текст сообщения бота.'
    msg = await callback_query.message.answer(text=text)
    await state.update_data({'query_msg': msg})


@update_router.message(TaskState.edit, F.content_type.in_({'text'}))
async def update_task_msg_content(message: types.Message, state: FSMContext):
    """Обновляет Информацию задачи"""
    # Очистка чата от сообщений
    await message.delete()
    data = await state.get_data()
    await data['query_msg'].delete()
    if message.text != data['task_msg'].text:
        kb = data['task_msg'].reply_markup
        new_msg = await data['task_msg'].edit_text(text=message.text, reply_markup=kb)
        await state.update_data({'task_msg': new_msg})
