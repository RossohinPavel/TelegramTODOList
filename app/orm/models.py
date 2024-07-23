from sqlalchemy import text, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = 'app_tasks'

    # Техническая информация
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Связка с пользователем телеграм
    telegram_id: Mapped[int] = mapped_column(BigInteger(), index=True)
    message_id: Mapped[int] = mapped_column(BigInteger(), index=True)
    
    # Временная метка сообщения
    creation_time: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

    # Контент
    content: Mapped[str]
