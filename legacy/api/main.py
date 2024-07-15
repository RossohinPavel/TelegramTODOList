import asyncio
from asyncio import StreamReader, StreamWriter
from os import getenv
from app import DataSerializer


class ConnectionProtocol:
    """Описание протокола соединеия"""
    __slots__ = ('_reader', '_writer', '_buffer_size')
    ECHO = getenv('API_ECHO', False)

    def __init__(self, reader: StreamReader, writer: StreamWriter, buffer_size: int = 2):
        self._reader = reader
        self._writer = writer
        self._buffer_size = buffer_size

    async def __aenter__(self):
        if self.ECHO: print("Connected")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if isinstance(exc_type, ConnectionError) and self.ECHO:
            print(f"Client suddenly closed socket")
        self._writer.close()
        if self.ECHO: print("Disconnected")
    
    async def read(self):
        """Читает данные с сокета"""
        buffer = await self._reader.read(n=self._buffer_size)
        return await self._reader.read(n=int.from_bytes(buffer))

    async def write(self, binary_data: bytes):
        """Отправляет данные на сокет"""
        buffer = len(binary_data).to_bytes(length=self._buffer_size)
        self._writer.write(buffer)
        await self._writer.drain()
        self._writer.write(binary_data)
        await self._writer.drain()


async def handle_connection(reader: StreamReader, writer: StreamWriter):
    """Обработка подключения"""
    async with ConnectionProtocol(reader, writer) as conn:
        binary_data = await conn.read()
        serializer = DataSerializer(binary_data)
        await serializer.clean()
        await conn.write(serializer.cleaned_data)


async def main(host, port):
    server = await asyncio.start_server(handle_connection, host, port)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main(
        getenv('API_HOST', ''),
        getenv('API_PORT')
    ))
