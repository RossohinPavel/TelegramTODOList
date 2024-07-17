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

    # Связка с пользователем телеграм
    telegram_id: Mapped[int] = mapped_column(index=True)

    # Контент
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str | None]
