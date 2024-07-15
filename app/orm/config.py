from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from os import getenv


class Settings:
    # Получаем хост и порт из окружения контейнера
    HOST: str = str(getenv("POSTGRES_HOST", ""))
    PORT: str = str(getenv("POSTGRES_PORT", ""))
    USER: str = str(getenv("POSTGRES_USER", ""))
    PASS: str = str(getenv("POSTGRES_PASSWORD", ""))
    NAME: str = str(getenv("POSTGRES_NAME", ""))

    @property
    def DATABASE_ASYNC_URL(self) -> str:
        return f'postgresql+asyncpg://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}'


settings = Settings()

# echo - просмотр sql запросов в консоли. в проде можно отключить
engine = create_async_engine(settings.DATABASE_ASYNC_URL, echo=True)

# Сессия
BaseSession = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False) #type: ignore
