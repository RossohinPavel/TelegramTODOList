from sqlalchemy import Column, Integer, DateTime, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func
from .config import Base


class User(Base):
    """Пользователи сервиса"""
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True)
    phone_number = Column(String(15), nullable=False, unique=True, index=True)
    telegram_id = Column(Integer, index=True)
    tasks = relationship('Task', back_populates='user')


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='tasks')

    title = Column(String(length=255), nullable=False, )
    description = Column(Text, default='')

    created_on = Column(DateTime(timezone=True), default=func.now())
    actual_on = Column(DateTime(timezone=True), nullable=False)
    finish_by = Column(DateTime(timezone=True), nullable=False)

    executed = Column(Boolean(), default=False)

    @validates("actual_on")
    def validate_actual_on(self, key, value):
        if self.finish_by is not None and value >= self.finish_by:
            raise ValueError("finish_by should be great then actual_on")
        return value

    @validates("finish_by")
    def validate_finish_by(self, key, value):
        if self.actual_on is not None and value <= self.actual_on:
            raise ValueError("finish_by should be great then actual_on")
        return value
