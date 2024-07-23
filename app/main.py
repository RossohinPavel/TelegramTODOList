import asyncio
from aiogram import Bot, Dispatcher
from os import getenv
from bot.routers import routers
from bot.middleware import CallbackExceptionHablerMiddleware
from bot import service


BOT = Bot(token=getenv('BOT_TOKEN'))
DP = Dispatcher()

# Добавляем в корневой роутер кастомные
DP.include_routers(*routers)
DP.callback_query.middleware(CallbackExceptionHablerMiddleware())


async def main():
    await asyncio.gather(DP.start_polling(BOT), service.message_resender(BOT))


if __name__ == "__main__":
    asyncio.run(main())
