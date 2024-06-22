#!/bin/sh
echo --Ожидание подключения к базе данных Postgress
# ./wait-for
echo --Подключено. Применяются миграции
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
# exec "$@"