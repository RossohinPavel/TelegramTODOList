"""Скрип для обработки комманд терминала"""
# TODO: Вся эта шляпа в основном для того, чтобы первое время добавлять пользователей
import sys


def manage_help():
    """Отображаем команды"""
    yield from (
        "help - Вывести список доступных комманд",
    )


def error_message(param: str):
    yield from (
        f"Неизвестная комманда {param}",
        "Используйте help для получения известных комманд"
    )


if __name__ == '__main__':
    _, *param = sys.argv
    if not param:
        param.append('help')

    match param[0]:
        case 'help':
            output = manage_help()
        case _:
            output = error_message(param[0])

    print(*output, sep='\n')
