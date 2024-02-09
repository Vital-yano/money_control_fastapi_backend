import asyncio
import json
from datetime import UTC, datetime

import asyncpg
import pytest
from redis.asyncio.client import Redis
from redis.asyncio.connection import ConnectionPool
from redis.commands.json.path import Path
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.sql import text
from starlette.testclient import TestClient

from config import (
    ALEMBIC_TEST_DATABASE_URL,
    REDIS_TEST_CONFIG,
    SQLALCHEMY_TEST_DATABASE_URL,
    USER_REGISTRATION_TIMEDELTA,
)
from main import app
from src.db import get_db, get_redis
from src.handlers import get_code

CLEAN_TABLES = [
    "user_account",
]


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


async def _get_test_db():
    test_engine = create_async_engine(
        SQLALCHEMY_TEST_DATABASE_URL, future=True, echo=True
    )

    test_async_session = async_sessionmaker(
        test_engine, expire_on_commit=False, class_=AsyncSession
    )
    yield test_async_session()
    await test_async_session().close()


async def _get_test_redis():
    redis_client = Redis(**REDIS_TEST_CONFIG)
    yield redis_client
    await redis_client.aclose()


def _generate_test_code():
    return "1234"


@pytest.fixture(scope="function")
def client():
    """
    Fixture creates test client with overrided dependencies
    """

    app.dependency_overrides[get_db] = _get_test_db
    app.dependency_overrides[get_redis] = _get_test_redis
    app.dependency_overrides[get_code] = _generate_test_code
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
async def async_session_test():
    test_engine = create_async_engine(
        SQLALCHEMY_TEST_DATABASE_URL, future=True, echo=True
    )
    async_session = async_sessionmaker(
        test_engine, expire_on_commit=False, class_=AsyncSession
    )
    yield async_session


@pytest.fixture(scope="function", autouse=True)
async def clean_tables(async_session_test):
    async with async_session_test() as session:
        async with session.begin():
            for table_for_cleaning in CLEAN_TABLES:
                await session.execute(text(f"""TRUNCATE TABLE {table_for_cleaning};"""))


@pytest.fixture(scope="session")
async def asyncpg_pool():
    pool = await asyncpg.create_pool(ALEMBIC_TEST_DATABASE_URL)
    yield pool
    if pool:
        await pool.close()


@pytest.fixture
async def create_user_in_database(asyncpg_pool):
    async def create_user_in_database(
        id: str, tg_id: str, phone_number: str, tg_nickname: str
    ):
        async with asyncpg_pool.acquire() as connection:
            return await connection.execute(
                """INSERT INTO user_account VALUES ($1, $2, $3, $4)""",
                id,
                tg_id,
                phone_number,
                tg_nickname,
            )

    return create_user_in_database


@pytest.fixture
async def get_user_from_database(asyncpg_pool):
    async def get_user_from_database_by_tg_id(tg_id: str):
        async with asyncpg_pool.acquire() as connection:
            return await connection.fetch(
                """SELECT * FROM user_account WHERE tg_id = $1;""", tg_id
            )

    return get_user_from_database_by_tg_id


@pytest.fixture(scope="session")
async def redis_pool():
    pool = ConnectionPool.from_url(
        f"redis://:{REDIS_TEST_CONFIG['password']}@{REDIS_TEST_CONFIG['host']}:{REDIS_TEST_CONFIG['port']}/0"
    )
    redis_client = Redis.from_pool(pool)
    yield redis_client
    await redis_client.aclose()


@pytest.fixture
async def get_user_from_redis(redis_pool):
    async def get_user_from_redis_by_tg_id(tg_id: str):
        user_from_redis = (
            await redis_pool.ft(index_name="idx:user").search(tg_id)
        ).docs[0]
        user_from_redis = json.loads(user_from_redis.json)
        return user_from_redis

    return get_user_from_redis_by_tg_id


@pytest.fixture(scope="function", autouse=True)
async def clean_redis(redis_pool):
    await redis_pool.json().delete(Path.root_path())  # type: ignore


@pytest.fixture
async def add_user_to_redis(redis_pool):
    async def add_user_to_redis(
        tg_id: str, phone_number: str, tg_nickname: str, verification_code: int
    ) -> dict:
        new_user = {
            "tg_id": tg_id,
            "phone_number": phone_number,
            "tg_nickname": tg_nickname,
            "verification_code": verification_code,
            "expire_at": datetime.strftime(
                datetime.now(UTC) + USER_REGISTRATION_TIMEDELTA, "%Y-%m-%d %H:%M:%S"
            ),
        }

        await redis_pool.json().set(  # type: ignore
            f"user:{new_user['tg_id']}", Path.root_path(), new_user
        )

        return new_user

    return add_user_to_redis
