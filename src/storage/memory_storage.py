import datetime
from typing import Any

from src.storage import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage as AiogramMemoryStorage


class MemoryStorage(BaseStorage, AiogramMemoryStorage):
    __storage: dict[str, Any] = {}
    __ttl: dict[str, Any] = {}

    async def delete(self, name: str):
        del self.__storage[name]

    async def set(self, name: str, value: Any, ttl: int = 300):
        self.__storage[name] = value
        self.__ttl[name] = datetime.datetime.now() + datetime.timedelta(seconds=ttl)

    async def get(self, name: str) -> Any | None:
        if name in self.__ttl:
            if datetime.datetime.now() > self.__ttl[name]:
                await self.delete(name)
                return None

        return self.__storage.get(name, None)
