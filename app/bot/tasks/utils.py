"""Набор утилит для работы с задачами"""
from orm.models import Task


RED_CIRCLE = '🔴'
YELLOW_CIRCLE = '🟡'
WHITE_CIRCLE = '⚪️'


async def create_task_text(task: Task) -> str:
    """Формирует текст задачи для отображения"""
    desc = task.description or ''
    return f'{WHITE_CIRCLE} {task.title}\n{desc}'


async def parse_message_text(text: str) -> tuple[str, str | None]:
    """Парсит сообщение для выделения title и description"""
    title, *description = text.split('\n', maxsplit=1)
    return title, description[0] if description else None
