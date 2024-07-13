import asyncio
import aiohttp
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from os import getenv

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=getenv('BOT_TOKEN'))
# Диспетчер
dp = Dispatcher()


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://api:8000', params={'phone_number': '79998887766'}) as resp:
            print(resp.status)
            await message.answer(str(await resp.json()))


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
