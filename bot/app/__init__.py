from .auth import auth_router
from .list import list_router
from .task import task_router


routers = (auth_router, list_router, task_router)
