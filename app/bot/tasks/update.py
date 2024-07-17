"""Набор скриптов для редактирования задачи"""
from aiogram import Router, types
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from orm import service
from . import keyboards


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
    data = {
        'id': callback_query.data[5:],
        'origin': callback_query.message.text
    }
    await state.set_data(data)
    kb = await keyboards.create_task_edit_keyboard()
    await callback_query.message.edit_reply_markup(reply_markup=kb)


@update_router.callback_query(TaskState.edit, lambda c: c.data and c.data.startswith('back'))
async def restore_task_content(callback_query: types.CallbackQuery, state: FSMContext):
    """Сбросить все изменения и восстановить текст задачи."""
    data = await state.get_data()
    kb = await keyboards.create_task_keyboard(data['id'])
    await callback_query.message.edit_text(text=data['origin'], reply_markup=kb)


@update_router.callback_query(TaskState.edit, lambda c: c.data and c.data.startswith('exec:'))
async def init_title_edit(callback_query: types.CallbackQuery, state: FSMContext):
    """Инициализация редактирования title задачи"""