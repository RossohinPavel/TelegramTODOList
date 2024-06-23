from datetime import datetime, timedelta
from django.urls import reverse


PATH = reverse('tasks-list', kwargs={'phone': '89998887766'})


def _get_currect_task(wt_shift: int = 1, fb_shift: int = 2) -> dict:
    """
    Возвращает словарь заполненной задачей.
    параметры shift - сдвиг по времени в часах
    wt_shift - для передачи задачи из очереди в актуальное
    fb_shift - для времени - закончить к
    """
    # Содержит только те поля, которые пользователь может менять непосредственно.
    dct = {
        'title': 'title',
        'description': 'description',
        'actual_time': datetime.now() + timedelta(wt_shift),
        'finish_by': datetime.now() + timedelta(fb_shift),
    }
    return dct
