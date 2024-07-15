from bot.common import common_router
from bot.users.auth import auth_router

routers = (
    common_router,
    auth_router,
)