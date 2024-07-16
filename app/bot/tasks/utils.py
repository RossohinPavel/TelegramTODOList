"""Набор утилит для работы с задачами"""
from orm.models import Task


RED_CIRCLE = '🔴'
YELLOW_CIRCLE = '🟡'
WHITE_CIRCLE = '⚪️'

LIST_MSG = 'Актуальные задачи:'
EMPTY_LIST_MSG = """Ваш список задач пуст.\n
Добавьте несколько задач, например, поход в магазин. 
В описании к задаче можно указать список покупок и отредактируйте время ее выполнения.\n
Организация задач позволит вам сосредоточиться на важном и интересном и нечего не забыть.
"""

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


async def get_tasks_text(task: Task) -> str:
    """Форматирует текст задачи"""
    text = await create_task_name(task)
    text += '\n'
    if task.description:
        text += task.description + '\n'
    text += 'Актуально с ' + str(task.actual_on) + '\n'
    text += 'Выполнить к ' + str(task.finish_by)
    return text
