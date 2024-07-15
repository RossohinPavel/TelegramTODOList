"""
В этом файле содержаться функции sqlalchemy, 
которые помогают при работе с базой данных.
"""
from sqlalchemy import select, text, insert
from .models import User, Task


# async def get_query_user(params: _BaseUserSchema) -> select:
#     """Возвращает запрос, который возвращает пользователя"""
#     return select(User).where(await _get_user_where_stmt(params))


async def get_query_user_id(**kwargs) -> select:
    """Возвращает запрос, который возварщает id пользователя."""
    return (
        select(User.id).
        where(await _get_user_where_stmt(**kwargs))
        # label('user_id')
    )


async def _get_user_where_stmt(**kwargs) -> text:
    """Формирует where-часть запроса для получения пользователя"""
    for key, value in kwargs.items():
        if value is not None:
            return text(f"{key}=:value").bindparams(value=value)


# async def get_query_tasks_list(params: _BaseUserSchema) -> select:
#     """Для получения списка невыполенных задач для пользователя"""
#     return (
#         select(Task.id, Task.title, Task.status)
#         .select_from(Task)
#         .where(
#             Task.user_id == await get_query_user_id(params),
#             Task.executed == False
#         )
#         .order_by(Task.finish_by)
#     )

# async def get_query_create_task(data: CreateTaskSchema, param: UserSchema) -> insert:
#     """Возвращает запрос для создания задачи"""
#     return (
#         insert(Task).
#         values(
#             **data.model_dump(exclude_none=True)
#         )
#     )