"""Общая настройка приложения и маршрутизации"""
from fastapi import FastAPI
from app import scripts
from app import users


app = FastAPI()


app.get('/user')(users.check_user)
app.post('/user')(users.create_user)



@app.get("/")
async def tasks_list(telegram_id: int):
    """Получение списка задач"""
    return {"message": f"Hello World - {telegram_id}"}