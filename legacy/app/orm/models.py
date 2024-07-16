from sqlalchemy import String, text, func, DateTime, ForeignKey, case, column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, validates, relationship, column_property
from typing import Annotated
from datetime import datetime


class Base(DeclarativeBase):
    pass


CREATED_AT = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
TIME = Annotated[datetime, mapped_column(DateTime(timezone=True))]


class User(Base):
    """Пользователи сервиса"""
    __tablename__ = 'users'

    # id он же telegram_id
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Информация о пользователе.
    name: Mapped[str] = mapped_column(default='Anon')
    surname: Mapped[str | None]
    phone_number: Mapped[str | None] = mapped_column(String(11), unique=True)

    # Техническая информация
    created_at: Mapped[CREATED_AT]

    # Связка с задачами
    # tasks: Mapped[list["Task"]] = relationship(back_populates="user")