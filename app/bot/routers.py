from bot.common import common_router
from bot.tasks.create import create_router
from bot.tasks.read import read_router

routers = (
    common_router,
    create_router,
    read_router
)