"""Общая настройка приложения и маршрутизации"""
from fastapi import FastAPI
from app import scripts
from app import users


app = FastAPI()


app.get('/users')(users.check_user)
app.post('/users', status_code=201)(users.create_user)
app.patch('/users/{user_id}', status_code=200)(users.update_user)
app.delete('/users/{user_id}', status_code=204)(users.delete_user)


@app.get("/")
async def tasks_list(telegram_id: int):
    """Получение списка задач"""
    return {"message": f"Hello World - {telegram_id}"}
