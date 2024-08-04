"""Набор скриптов для работы с созданием задачи"""
from aiogram import Router, types, F
from orm import service
from . import keyboards as kb
from audio.stt import STT
from . import utils


create_router = Router(name='__create_task__')


async def _create_task(message: types.Message, text: str):
    """Создает задачу"""
    await message.delete()
    task_message = await message.answer(text, reply_markup=kb.TASK_KEYBOARD)
    task = await service.create_task(task_message.chat.id, task_message.message_id, task_message.text)
    # В случае, если вернется ошибка.
    if isinstance(task, str):
        task_message.delete()
        await message.answer(text=task)


@create_router.message(F.text)
async def create_task_from_text(message: types.Message):
    """Инициализация создания задачи по текстовому вводу пользователя"""
    await _create_task(message, message.text)


@create_router.message(F.voice)
async def create_task_from_audio(message: types.Message):
    """Создание задачи из аудио сообщения"""
    audio_stream = await utils.get_file_binary(message.bot, message.voice.file_id)
    stt_obj = await STT.from_ogg_binary(audio_stream)
    text = await stt_obj.recognition()
    await _create_task(message, text)
