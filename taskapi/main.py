"""Общая настройка приложения и маршрутизации"""
from fastapi import FastAPI
from app import users, tasks


app = FastAPI()

# Работа с пользователями
app.get('/users')(users.check_user)                                 # Получение user'а по телефону или телеграм id
app.post('/users', status_code=201)(users.create_user)              # Создание пользователя
app.patch('/users/{user_id}', status_code=200)(users.update_user)   # Обновление информации о пользователе
app.delete('/users/{user_id}', status_code=204)(users.delete_user)  # Удаление пользователя

# Работа с задачами
app.get('/')(tasks.get_tasks_list)                              # Получение списка задач
app.post('/', status_code=201)(tasks.create_task)               # Создание задачи
app.get('/{task_id}')(tasks.get_task)                           # Получение информации по задаче
app.patch('/{task_id}', status_code=200)(tasks.update_task)     # Обновление информации по задаче
app.delete('/{task_id}', status_code=204)(tasks.delete_task)    # Удаление задачи