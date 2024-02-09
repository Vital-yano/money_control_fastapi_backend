import logging

from fastapi import APIRouter, Depends, HTTPException, status
from redis.asyncio.client import Redis
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.actions import (
    _add_user_to_redis,
    _create_new_user,
    _is_verified_code_and_registration_time,
    _send_code_via_call,
)
from src.db import get_db, get_redis
from src.schemas import (
    SendCodeSchema,
    ShowUserSchema,
    UserAddtoRedisSchema,
    UserCreateSchema,
)
from src.utils import get_code

logger = logging.getLogger(__name__)

user_router = APIRouter()


@user_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(
    body: UserCreateSchema,
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
) -> ShowUserSchema | None:
    is_verified_code_and_registration_time = (
        await _is_verified_code_and_registration_time(body, redis)
    )
    if is_verified_code_and_registration_time:
        try:
            return await _create_new_user(body, db)
        except IntegrityError as err:
            logger.error(err)
            raise HTTPException(status_code=503, detail=f"Database error: {err}")


@user_router.post("/send_code", status_code=status.HTTP_200_OK)
async def send_code(
    body: UserAddtoRedisSchema,
    redis: Redis = Depends(get_redis),
    generated_test_code: str | None = Depends(get_code),
) -> SendCodeSchema:
    if generated_test_code:
        verification_code = generated_test_code
    else:
        verification_code = await _send_code_via_call(body)
    await _add_user_to_redis(body, redis, verification_code)
    return SendCodeSchema(code=verification_code)
