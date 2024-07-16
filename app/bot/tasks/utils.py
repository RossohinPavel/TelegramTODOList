"""Набор утилит для работы с задачами"""
from orm.models import Task


RED_CIRCLE = '🔴'
YELLOW_CIRCLE = '🟡'
WHITE_CIRCLE = '⚪️'


async def create_task_name(task: Task) -> str:
    """Формирует имя задачи для отображения в списке"""
    match task.status:
        case 2: circle = RED_CIRCLE
        case 1: circle = YELLOW_CIRCLE
        case 0 | _: circle = WHITE_CIRCLE
    # Обрезаем имя задачи, если оно слишком длинное
    title = task.title
    if len(title) > 20:
        title = title[:17] + '...'
    return f'{circle} {title}' 
