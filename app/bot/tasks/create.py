"""Набор скриптов для работы с созданием задачи"""
from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from orm import service
from .task import _get_task_msg_content


create_router = Router(name='__create_task__')


class UserState(StatesGroup):
    create_task = State()


@create_router.message(Command('create'))
async def init_create_task(message: types.Message, state: FSMContext):
    """Инициализация создания задачи по запросу пользователя"""
    await state.set_state(UserState.create_task)
    await message.answer('Введите название задачи')


@create_router.message(UserState.create_task)
async def finish_create_task(message: types.Message, state: FSMContext):
    """Завершение создания задачи. Текст сообщения послужит title для задачи"""
    await state.clear()
    id = await service.create_task(message.from_user.id, message.text)
    text, keyboard = await _get_task_msg_content(id)
    await message.answer(text=text, reply_markup=keyboard)


@create_router.callback_query(F.data == 'create')
async def create_task_from_callback(callback_query: types.CallbackQuery, state: FSMContext):
    """Создание задачи по нажатию кнопки"""
    await callback_query.message.delete()
    await init_create_task(callback_query.message, state)
