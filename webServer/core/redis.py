from typing import Optional

from arq import create_pool
from arq.connections import ArqRedis, RedisSettings
from fastapi import Request

from core.config import Settings


class Redis:
    def __init__(self):
        self.pool: Optional[ArqRedis] = None

    async def create_redis_pool(self):
        self.pool = await create_pool(
            RedisSettings(host=Settings.REDIS_HOST, port=Settings.REDIS_PORT)
        )

    async def close_redis_pool(self):
        self.pool.close()


def get_redis(request: Request) -> Redis:
    return request.app.state.redis
