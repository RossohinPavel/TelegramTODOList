"""Общая настройка приложения и маршрутизации"""
from fastapi import FastAPI
from app.users import users_router
from app.tasks import tasks_router


app = FastAPI()
app.include_router(users_router)
app.include_router(tasks_router)
