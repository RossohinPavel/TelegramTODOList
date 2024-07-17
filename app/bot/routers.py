from bot.common import common_router
from bot.tasks.create import create_router
from bot.tasks.update import update_router


routers = (
    common_router,
    create_router,
    update_router
)