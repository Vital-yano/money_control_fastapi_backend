from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import ShowUserSchema, UserAddtoRedisSchema, UserCreateSchema
from src.user_dal import UserDbDal, UserRedisDAL


async def _create_new_user(
    body: UserCreateSchema, session: AsyncSession
) -> ShowUserSchema:
    async with session.begin():
        user_dal = UserDbDal(session)
        user = await user_dal.create_user(
            tg_id=body.tg_id,
            phone_number=body.phone_number,
            tg_nickname=body.tg_nickname,
        )
    return ShowUserSchema(
        id=user.id,
        tg_id=user.tg_id,
        phone_number=user.phone_number,
        tg_nickname=user.tg_nickname,
    )


async def _add_user_to_redis(
    body: UserAddtoRedisSchema, redis_client, verification_code
):
    user_redis_dal = UserRedisDAL(redis_client)
    await user_redis_dal.create_user(
        tg_id=body.tg_id,
        phone_number=body.phone_number,
        tg_nickname=body.tg_nickname,
        verification_code=verification_code,
    )


async def _is_verified_code_and_registration_time(
    body: UserCreateSchema, redis_client
) -> bool:
    user_redis_dal = UserRedisDAL(redis_client)
    redis_user = await user_redis_dal.get_user(body.tg_id)
    expire_at = datetime.strptime(redis_user["expire_at"], "%Y-%m-%d %H:%M:%S")

    if body.verification_code != redis_user["verification_code"]:
        raise HTTPException(status_code=422, detail="Wrong verification code")

    if body.registration_time > expire_at:
        raise HTTPException(
            status_code=422, detail="The code has expired. Request new code"
        )
    return True
