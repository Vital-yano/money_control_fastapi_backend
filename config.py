import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

ALEMBIC_TEST_DATABASE_URL = "postgresql://postgres_test_local:postgres_test_local@localhost:5433/postgres_test_local"
ALEMBIC_DATABASE_URL = (
    "postgresql://postgres_local:postgres_local@localhost:5432/postgres_local"
)

SQLALCHEMY_TEST_DATABASE_URL = "postgresql+asyncpg://postgres_test_local:postgres_test_local@localhost:5433/postgres_test_local"
SQLALCHEMY_DATABASE_URL = (
    "postgresql+asyncpg://postgres_local:postgres_local@localhost:5432/postgres_local"
)

SMS_API_ID = os.getenv("SMS_API_ID")

REDIS_CONFIG = {
    "host": "localhost",
    "port": 6379,
    "password": "redis_local",
    "decode_responses": True,
}

REDIS_TEST_CONFIG = {
    "host": "localhost",
    "port": 6380,
    "password": "redis_test",
    "decode_responses": True,
}

USER_REGISTRATION_TIMEDELTA = timedelta(minutes=5)
