from bot.common import common_router
from bot.tasks.create import create_router
from bot.tasks.list import list_router
from bot.tasks.task import task_router
from bot.tasks.edit import edit_router

routers = (
    common_router,
    create_router,
    list_router,
    task_router,
    edit_router
)