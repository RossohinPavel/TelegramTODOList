from sqlalchemy import String, text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Annotated
from datetime import datetime



# from sqlalchemy import Column, Integer, DateTime, Text, ForeignKey, Boolean
# from sqlalchemy.orm import relationship, validates
# from sqlalchemy.ext.hybrid import hybrid_property



class Base(DeclarativeBase):
    pass


INTPK = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
CREATED_AT = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]


class User(Base):
    """Пользователи сервиса"""
    __tablename__ = 'users'

    id: Mapped[INTPK]
    created_at: Mapped[CREATED_AT]

    phone_number: Mapped[str] = mapped_column(String(11), index=True, nullable=False, unique=True)
    telegram_id: Mapped[int | None] = mapped_column(index=True)


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[INTPK]
    created_at: Mapped[CREATED_AT]
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=func.utc_timestamp()
    )
    # Контент
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str | None]
    executed: Mapped[bool] = mapped_column(default=False)

    # actual_on = Column(DateTime(timezone=True), nullable=False)
    # finish_by = Column(DateTime(timezone=True), nullable=False)

    # executed = Column(Boolean(), default=False)

    # user_id = Column(Integer, ForeignKey('users.id'))
    # user = relationship('User', back_populates='tasks')

    # actual_on = Column(DateTime(timezone=True), nullable=False)
    # finish_by = Column(DateTime(timezone=True), nullable=False)

    # executed = Column(Boolean(), default=False)

    # @validates("actual_on")
    # def validate_actual_on(self, key, value):
    #     if self.finish_by is not None and value >= self.finish_by:
    #         raise ValueError("finish_by should be great then actual_on")
    #     return value

    # @validates("finish_by")
    # def validate_finish_by(self, key, value):
    #     if self.actual_on is not None and value <= self.actual_on:
    #         raise ValueError("finish_by should be great then actual_on")
    #     return value
    
    # @hybrid_property
    # def status(self):
    #     return self.id
