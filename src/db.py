from typing import AsyncGenerator

from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

import config


async_engine = create_async_engine(
    url=config.SQLALCHEMY_DATABASE_URL,
    future=True,
    echo=True,
    execution_options={"isolation_level": "AUTOCOMMIT"},
)

async_session = async_sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)


async def get_db() -> AsyncGenerator | None:
    """Dependency для получения сессии бд"""
    session = None

    try:
        session: AsyncSession | None = async_session()
        yield session
    finally:
        if session:
            await session.close()


async def get_redis() -> AsyncGenerator | None:
    """Dependency для получения клиента redis"""
    redis_client = None

    try:
        redis_client: Redis | None = Redis(**config.REDIS_CONFIG)
        yield redis_client
    finally:
        if redis_client:
            await redis_client.close()
