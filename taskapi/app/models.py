from sqlalchemy import String, text, func, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, validates
from typing import Annotated
from datetime import datetime


class Base(DeclarativeBase):
    pass


CREATED_AT = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
TIME = Annotated[datetime, mapped_column(DateTime(timezone=True))]


class User(Base):
    """Пользователи сервиса"""
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[CREATED_AT]

    phone_number: Mapped[str] = mapped_column(String(11), index=True, unique=True)
    telegram_id: Mapped[int | None] = mapped_column(index=True)


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    created_at: Mapped[CREATED_AT]
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=func.utc_timestamp()
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    # Контент
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str | None]
    executed: Mapped[bool] = mapped_column(default=False)
    actual_on: Mapped[TIME]
    finish_by: Mapped[TIME]

    @validates("actual_on")
    def validate_actual_on(self, key, value):
        self.validate_time(value, self.finish_by)
        return value

    @validates("finish_by")
    def validate_finish_by(self, key, value):
        self.validate_time(self.actual_on, value)
        return value
    
    def validate_time(self, actual_on: datetime, finish_by: datetime) -> None:
        """Функция для сравнения времени"""
        if actual_on is None or finish_by is None:
            return
        if actual_on >= finish_by:
            raise ValueError("finish_by should be great then actual_on")
    
    # @hybrid_property
    # def status(self):
    #     return self.id
