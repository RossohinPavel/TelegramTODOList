"""Скрипт для работы с задачами"""
from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from .connection import Serializer
from .middleware import ExceptionHandlerMiddleware
from datetime import UTC, datetime, timedelta


task_router = Router(name='__task__')
task_router.message.middleware(ExceptionHandlerMiddleware())


class UserState(StatesGroup):
    create_task = State()


@task_router.message(Command('create'))
async def cmd_create(message: types.Message, state: FSMContext):
    """Инициализация создания задачи"""
    req = {
        'func': 'get_user_id',
        'params': {'telegram_id': message.from_user.id}
    }
    s = Serializer(req)
    await s.connect()
    if s.response_data is None:
        raise ValueError('User not found')

    await state.set_state(UserState.create_task)
    await state.update_data(user_id=s.response_data)
    await message.answer('Введите название задачи')


@task_router.message(UserState.create_task)
async def create_task(message: types.Message, state: FSMContext):
    """Создание задачи по введеному сообщению"""
    params = await state.get_data()
    params['title'] = message.text
    now = datetime.now(UTC)
    params['actual_on'] = now
    params['finish_by'] = now + timedelta(days=1)
    req = {'func': 'create_task', 'params': params}
    s = Serializer(req)
    await s.connect()
    await state.clear()
    await message.answer(str(s.response_data))
