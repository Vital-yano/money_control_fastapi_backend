import json
from datetime import UTC, datetime

from redis.asyncio.client import Redis
from redis.commands.json.path import Path
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.exceptions import ResponseError
from sqlalchemy.ext.asyncio import AsyncSession

from config import USER_REGISTRATION_TIMEDELTA
from src.models import User, redis_schema


class UserDbDal:
    """Data Access Layer для операций с пользователями в db"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
        self, tg_id: str, phone_number: str, tg_nickname: str
    ) -> User:
        new_user = User(tg_id=tg_id, phone_number=phone_number, tg_nickname=tg_nickname)
        self.db_session.add(new_user)
        await self.db_session.flush()

        return new_user


class UserRedisDAL:
    """Data Access Layer для операций с пользователями в Redis"""

    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    async def create_user(
        self, tg_id: str, phone_number: str, tg_nickname: str, verification_code: int
    ) -> dict:
        index = self.redis_client.ft("idx:user")
        try:
            await index.create_index(
                redis_schema,
                definition=IndexDefinition(prefix=["user:"], index_type=IndexType.JSON),
            )
        except ResponseError as exc:
            if exc.args[0] == "Index already exists":
                pass

        new_user = {
            "tg_id": tg_id,
            "phone_number": phone_number,
            "tg_nickname": tg_nickname,
            "verification_code": verification_code,
            "expire_at": datetime.strftime(
                datetime.now(UTC) + USER_REGISTRATION_TIMEDELTA, "%Y-%m-%d %H:%M:%S"
            ),
        }

        await self.redis_client.json().set(  # type: ignore
            f"user:{new_user['tg_id']}", Path.root_path(), new_user
        )

        return new_user

    async def get_user(self, tg_id: str) -> dict:
        user_from_redis = (
            await self.redis_client.ft(index_name="idx:user").search(tg_id)
        ).docs[0]
        user_from_redis = json.loads(user_from_redis.json)
        return user_from_redis
