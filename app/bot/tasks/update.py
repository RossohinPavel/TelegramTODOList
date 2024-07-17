"""Набор скриптов для редактирования задачи"""
from aiogram import Router, types, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from orm import service
from . import keyboards
from . import utils


class TaskState(StatesGroup):
    edit = State()


update_router = Router(name='__update__')


@update_router.callback_query(lambda c: c.data and c.data.startswith('exec:'))
async def execute_task(callback_query: types.CallbackQuery):
    """Ловит калбэк с клавиатуры и выполняет задачу"""
    await callback_query.message.delete()
    task_name, *_ = callback_query.message.text.split('\n', maxsplit=1)
    await callback_query.answer(text=f'Задача <{task_name}> выполнена.')
    await service.execute_task(callback_query.data[5:])


@update_router.callback_query(lambda c: c.data and c.data.startswith('edit:'))
async def init_edit(callback_query: types.CallbackQuery, state: FSMContext):
    """Инициализация редактирования задачи"""
    await state.set_state(TaskState.edit)
    kb = await keyboards.create_task_edit_keyboard()
    msg = await callback_query.message.edit_reply_markup(reply_markup=kb)
    data = {
        'id': callback_query.data[5:],
        'origin': msg.text,
        'task_msg': msg,
        'query_msg': None,
        'part': None
    }
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
        title, description = await utils.parse_message_text(data['task_msg'].text)
        await service.update_task(data['id'], title[2:], description)
    else:
        await callback_query.message.edit_text(text=data['origin'])
    kb = await keyboards.create_task_keyboard(data['id'])
    await callback_query.message.edit_reply_markup(reply_markup=kb)


@update_router.callback_query(TaskState.edit, F.data.in_({'title', 'desc'}))
async def init_task_title_edit(callback_query: types.CallbackQuery, state: FSMContext):
    """Инициализация редактирования задачи"""
    match callback_query.data:
        case 'title': text = 'Введите новое имя'
        case 'desc' | _: text = 'Введите новое описание'
    msg = await callback_query.message.answer(text=text)
    await state.update_data({'query_msg': msg, 'part': callback_query.data})


@update_router.message(TaskState.edit, F.content_type.in_({'text'}))
async def update_task_msg_content(message: types.Message, state: FSMContext):
    """Обновляет Информацию задачи"""
    data = await state.get_data()
    # Очистка чата от сообщений
    await message.delete()
    await data['query_msg'].delete()
    data = await state.get_data()
    title, desc = await utils.parse_message_text(data['task_msg'].text)
    match data['part']:
        case 'title': title = await utils.format_task_title(message.text)
        case 'desc' | _: desc = message.text
    text = f'{title}\n{desc or ""}'
    kb = data['task_msg'].reply_markup
    new_msg = await data['task_msg'].edit_text(text=text, reply_markup=kb)
    await state.update_data({'task_msg': new_msg})
