"""Модуль для аутенфикации пользователя"""
from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from orm import service


auth_router = Router(name='__auth__')


START_MSG = """Тебя приветствует бот-помощник в организации задач!
Чтобы воспользоваться моими услугами нужно зарегистрировать аккаунт.
Нажми на /register или введи эту комманду.
"""


@auth_router.message(Command('start'))
async def cmd_start(message: types.Message):
    """Проверяет пользователя по id и в зависимости от этого отправляет сообщение."""
    msg = START_MSG
    user = await service.get_user(message.from_user.id)
    if user is not None:
        msg = f'{user.name}, с возвращением!'
    await message.answer(msg)


@auth_router.message(Command('register'))
async def cmd_register(message: types.Message):
    """Отправка клавиатуры для отправки контакта."""
    msg = """Подтвердите свой аккаунт нажав на всплывающую клавиатуру в поле ввода."""
    await message.answer(text=msg, reply_markup=await contact_keyboard())


async def contact_keyboard():
    """Формирование клавиатуры отправки контакта"""
    kb = ReplyKeyboardBuilder()
    kb.button(text='Отправить контакт', request_contact=True)
    return kb.as_markup(resize_keyboard=True)


@auth_router.message(F.content_type.in_({'contact'}))
async def handle_contact(message: types.Message):
    """Обработка входящих контактов"""
    kb = None
    if message.from_user.id == message.contact.user_id:
        msg = await create_user(message.contact)
        kb = types.reply_keyboard_remove.ReplyKeyboardRemove()
    else:
        msg = "Ошибка. Контакт не совпадает с отправителем"
    await message.answer(text=msg, reply_markup=kb)


async def create_user(contact: types.Contact) -> str:
    """Формирует запрос к sqlalchemy для регистрации пользователя."""
    kwargs = {}
    if contact.first_name:
        kwargs['name'] = contact.first_name
    if contact.last_name:
        kwargs['surname'] = contact.last_name
    if contact.phone_number:
        kwargs['phone_number'] = contact.phone_number
    
    user = await service.create_user(contact.user_id, **kwargs)
    if isinstance(user, str):
        return user
    return f'Регистрация успешна. Можно пользоваться сервисом.'
