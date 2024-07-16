from sqlalchemy import String, text, DateTime, case, column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, column_property
from typing import Annotated
from datetime import datetime


class Base(DeclarativeBase):
    pass


NOW = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]


class Task(Base):
    __tablename__ = 'app_tasks'

    # Техническая информация
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    created_at: Mapped[NOW]
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=text("TIMEZONE('utc', now())")
    )

    # Связка с пользователем телеграм
    telegram_id: Mapped[int] = mapped_column(index=True)

    # Контент
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str | None]

    # Временные метки задачи
    # С виду дублирует функционал сreated_at, но это поле изменяемое. Отложение выполения задачи
    actual_on: Mapped[NOW]  
    # На старте, отложим время выполнения пока на 1 день
    finish_by: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('utc', now() + interval '1 day')")
    )

    # Метка о выполнении задачи
    executed: Mapped[bool] = mapped_column(default=False)

    # Вычисляемое поле. Пока в таком виде
    status: Mapped[int] = column_property(
        case(
            (text("TIMEZONE('utc', now())") > column('finish_by'), 2),
            (text("TIMEZONE('utc', now())") > column('actual_on'), 1),
            else_=0
        ).label('status')
    )
