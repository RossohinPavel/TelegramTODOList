"""Содержит класс описывающий протокол подключения"""
import asyncio
import pickle
from os import getenv


class Connection:
    """Клиентская часть протокола связи"""

    __slots__ = ('_reader', '_writer', '_buffer_size')

    _reader: asyncio.StreamReader
    _writer: asyncio.StreamWriter

    HOST = getenv('API_HOST', '')
    PORT = getenv('API_PORT')

    def __init__(self, buffer_size: int = 2) -> None:
        self._buffer_size = buffer_size

    async def __aenter__(self):
        self._reader, self._writer = await asyncio.open_connection(self.HOST, self.PORT)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._writer.close()

    async def read(self):
        """Читаем информацию из буфера"""
        buffer = await self._reader.read(n=self._buffer_size)
        return await self._reader.read(n=int.from_bytes(buffer))
    
    async def write(self, binary_data: bytes):
        """Отправляет данные на сокет"""
        buffer = len(binary_data).to_bytes(length=self._buffer_size)
        self._writer.write(buffer)
        await self._writer.drain()
        self._writer.write(binary_data)
        await self._writer.drain()


class Serializer:
    """Обертка над Connection для более удобного использования подключения."""

    __slots__ = ('request_data', 'response_data')

    def __init__(self, request_data):
        self.request_data = request_data
        self.response_data = None

    async def connect(self):
        """Переводит данные в бинарный формат, связывается с сервером и ждет ответ."""
        binary_data = pickle.dumps(self.request_data, pickle.HIGHEST_PROTOCOL)
        async with Connection() as conn:  
            await conn.write(binary_data)
            response_binary = await conn.read()
        self.response_data = pickle.loads(response_binary)