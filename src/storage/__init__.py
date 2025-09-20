__all__ = [
    "BaseStorage",
    "create_bot_storage"
]

import codecs
import pickle

from redis.asyncio.client import Redis

from src.config import IS_PROD, REDIS_HOST, REDIS_PORT, REDIS_TTL
from src.storage.base_storage import BaseStorage
from src.storage.redis_storage import RedisStorage
from src.storage.memory_storage import MemoryStorage

def create_bot_storage() -> BaseStorage:
    storage: BaseStorage = MemoryStorage()

    if IS_PROD:
        redis = Redis(host=REDIS_HOST, port=REDIS_PORT)
        ttl = 60 * 60 * REDIS_TTL
        storage = RedisStorage(
            redis=redis,
            state_ttl=ttl,
            data_ttl=ttl,
            json_dumps=lambda x: codecs.encode(pickle.dumps(x), "base64").decode(),
            json_loads=lambda x: pickle.loads(codecs.decode(x.encode(), "base64")),
        )

    return storage
