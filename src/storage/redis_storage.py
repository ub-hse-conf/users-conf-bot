from typing import Any

from aiogram.fsm.storage.redis import RedisStorage as AiogramRedisStorage
from redis.asyncio.client import Redis

from src.storage import BaseStorage


class RedisStorage(BaseStorage, AiogramRedisStorage):
    def __init__(self, redis: Redis, *args, **kwargs):
        super().__init__(redis=redis, *args, **kwargs)

    async def get(self, name: str) -> Any | None:
        return await self.redis.get(name)

    async def set(self, name: str, value: Any, ttl: int = 300) -> None:
        await self.redis.set(name, value, ex=ttl)

    async def delete(self, name: str, version: int = 0) -> None:
        await self.redis.delete(name)
