from typing import Any


class BaseStorage:
    async def get(self, name: str) -> Any | None:
        raise NotImplementedError

    async def set(self, name: str, value: Any, ttl: int = 300) -> None:
        raise NotImplementedError

    async def delete(self, name):
        raise NotImplementedError