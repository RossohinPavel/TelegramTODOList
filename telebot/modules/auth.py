"""Модуль для аутенфикации пользователя"""
from aiogram import Router
from aiogram.filters.command import Command
from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import F


auth_router = Router(name='__auth__')


@auth_router.message(Command('start'))
async def cmd_start(message: types.Message):
    msg = """Тебя приветствует бот-помощник!
Чтобы воспользоваться моими услугами нужно подтвердить аккаунт.
Нажми на /register или введи эту комманду.
    """
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


# Ловим контакты
@auth_router.message(F.content_type.in_({'contact'}))
async def handle_contact(message: types.Message):
    if message.from_user.id == message.contact.user_id:
        r, msg = await check_user(message.contact.phone_number, message.contact.user_id)
        if r:
            msg = "Контакт подтвержден. Вы можете пользоваться ботом."
        await message.answer(text=msg, reply_markup=types.reply_keyboard_remove.ReplyKeyboardRemove())

    else:
        await message.answer("Ошибка. Контакт не совпадает с отправителем")


async def check_user(phone: str, telegram_id: int) -> tuple[bool, str]:
    """Запрос к основному серверу для проверки пользователя."""
    return False, 'something wrong'