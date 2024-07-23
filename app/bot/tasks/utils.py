"""Набор утилит для работы с задачами"""
from orm.models import Task


RED_CIRCLE = '🔴'
YELLOW_CIRCLE = '🟡'
WHITE_CIRCLE = '⚪️'


async def create_task_text(task: Task) -> str:
    """Формирует текст задачи для отображения"""
    desc = task.description or ''
    return f'{await format_task_title(task.title)}\n{desc}'


async def format_task_title(title: str) -> str:
    """Форматирует текст заголовка задачи"""
    return f'{WHITE_CIRCLE} {title}'


async def parse_message_text(text: str) -> tuple[str, str | None]:
    """Парсит сообщение для выделения title и description"""
    title, *description = text.split('\n', maxsplit=1)
    return title, description[0] if description else None


async def reduce_task_content(text: str) -> str:
    """Сокращает тест задачи до 15 символов"""
    if len(text) > 12:
        text = text[:12] + '...'
    return text