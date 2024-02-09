import asyncio

from redis.asyncio.client import Redis

import config
from src.logging_setup import configure_logging
from src.user_dal import UserRedisDAL


async def init_index(user_redis_dal: UserRedisDAL):
    return await user_redis_dal.create_index()


async def main():
    configure_logging()
    redis_client_local = Redis(**config.REDIS_CONFIG)
    redis_client_test = Redis(**config.REDIS_TEST_CONFIG)
    user_redis_dal_local = UserRedisDAL(redis_client_local)  # type: ignore
    user_redis_dal_test = UserRedisDAL(redis_client_test)  # type: ignore
    await init_index(user_redis_dal_local)
    await init_index(user_redis_dal_test)
    await redis_client_local.aclose()
    await redis_client_test.aclose()


if __name__ == "__main__":
    asyncio.run(main())
