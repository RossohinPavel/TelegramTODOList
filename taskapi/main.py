"""Общая настройка приложения и маршрутизации"""
from fastapi import FastAPI
from app import scripts
from app import users


app = FastAPI()


app.get('/users')(users.check_user)
app.post('/users', status_code=201)(users.create_user)


@app.get("/")
async def tasks_list(telegram_id: int):
    """Получение списка задач"""
    return {"message": f"Hello World - {telegram_id}"}
