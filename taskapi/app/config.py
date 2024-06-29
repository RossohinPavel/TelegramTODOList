from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from os import getenv

# Получаем хост и порт из окружения контейнера
host: str = str(getenv("POSTGRES_HOST", ""))
port: int = int(getenv("POSTGRES_PORT", ""))
user: str = str(getenv("POSTGRES_USER", ""))
password: str = str(getenv("POSTGRES_PASSWORD", ""))

# Определяем движок для базы. Postgresql на asyncpg. 
# В URL вписываем адрес контейнера
# echo - просмотр sql запросов в консоли. в проде можно отключить
engine = create_async_engine(f'postgresql+asyncpg://{user}:{password}@{host}:{port}/taskapi', echo=True)

# База для моделей
Base = declarative_base()

# Сессия
BaseSession = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
