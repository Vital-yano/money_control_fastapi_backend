import json
import uuid
from datetime import UTC, datetime, timedelta

import pytest


async def test_create_user(client, get_user_from_database, add_user_to_redis):
    user_data = {
        "tg_id": "88005553535",
        "phone_number": "+79991234567",
        "tg_nickname": "pogchamp",
        "verification_code": 123456,
        "registration_time": datetime.strftime(datetime.now(UTC), "%Y-%m-%d %H:%M:%S"),
    }
    await add_user_to_redis(
        user_data["tg_id"],
        user_data["phone_number"],
        user_data["tg_nickname"],
        user_data["verification_code"],
    )
    response = client.post("/user/create", content=json.dumps(user_data))
    assert response.status_code == 201
    data_from_resp = response.json()
    assert data_from_resp["tg_id"] == user_data["tg_id"]
    assert data_from_resp["phone_number"] == user_data["phone_number"]
    assert data_from_resp["tg_nickname"] == user_data["tg_nickname"]
    users_from_db = await get_user_from_database(data_from_resp["tg_id"])
    assert len(users_from_db) == 1
    user_from_db = dict(users_from_db[0])
    assert user_from_db["tg_id"] == user_data["tg_id"]
    assert user_from_db["phone_number"] == user_data["phone_number"]
    assert user_from_db["tg_nickname"] == user_data["tg_nickname"]
    assert str(user_from_db["tg_id"]) == data_from_resp["tg_id"]


async def test_create_user_with_the_same_tg_id(
    client, create_user_in_database, get_user_from_database, add_user_to_redis
):
    user_data = {
        "id": uuid.uuid4(),
        "tg_id": "88005553535",
        "phone_number": "+79991234567",
        "tg_nickname": "pogchamp",
    }
    user_data_with_the_same_tg_id = {
        "tg_id": "88005553535",
        "phone_number": "+71234567890",
        "tg_nickname": "pogchamp2",
        "verification_code": 123456,
        "registration_time": datetime.strftime(datetime.now(UTC), "%Y-%m-%d %H:%M:%S"),
    }
    await create_user_in_database(
        user_data["id"],
        user_data["tg_id"],
        user_data["phone_number"],
        user_data["tg_nickname"],
    )
    users_from_db = await get_user_from_database(user_data["tg_id"])
    assert len(users_from_db) == 1
    user_from_db = dict(users_from_db[0])
    assert user_from_db["tg_id"] == user_data["tg_id"]
    assert user_from_db["phone_number"] == user_data["phone_number"]
    assert user_from_db["tg_nickname"] == user_data["tg_nickname"]
    await add_user_to_redis(
        user_data_with_the_same_tg_id["tg_id"],
        user_data_with_the_same_tg_id["phone_number"],
        user_data_with_the_same_tg_id["tg_nickname"],
        user_data_with_the_same_tg_id["verification_code"],
    )
    resp = client.post(
        "/user/create", content=json.dumps(user_data_with_the_same_tg_id)
    )
    assert resp.status_code == 503
    assert (
        'duplicate key value violates unique constraint "user_account_tg_id_key"'
        in resp.json()["detail"]
    )


async def test_create_user_with_the_same_phone_number(
    client, create_user_in_database, get_user_from_database, add_user_to_redis
):
    user_data = {
        "id": uuid.uuid4(),
        "tg_id": "88005553535",
        "phone_number": "+79991234567",
        "tg_nickname": "pogchamp",
    }
    user_data_with_the_same_phone_number = {
        "tg_id": "2323909093",
        "phone_number": "+79991234567",
        "tg_nickname": "pogchamp2",
        "verification_code": 123456,
        "registration_time": datetime.strftime(datetime.now(UTC), "%Y-%m-%d %H:%M:%S"),
    }
    await create_user_in_database(
        user_data["id"],
        user_data["tg_id"],
        user_data["phone_number"],
        user_data["tg_nickname"],
    )
    users_from_db = await get_user_from_database(user_data["tg_id"])
    assert len(users_from_db) == 1
    user_from_db = dict(users_from_db[0])
    assert user_from_db["tg_id"] == user_data["tg_id"]
    assert user_from_db["phone_number"] == user_data["phone_number"]
    assert user_from_db["tg_nickname"] == user_data["tg_nickname"]
    await add_user_to_redis(
        user_data_with_the_same_phone_number["tg_id"],
        user_data_with_the_same_phone_number["phone_number"],
        user_data_with_the_same_phone_number["tg_nickname"],
        user_data_with_the_same_phone_number["verification_code"],
    )
    resp = client.post(
        "/user/create", content=json.dumps(user_data_with_the_same_phone_number)
    )
    assert resp.status_code == 503
    assert (
        'duplicate key value violates unique constraint "user_account_phone_number_key"'
        in resp.json()["detail"]
    )


@pytest.mark.parametrize(
    "user_data_for_creation, expected_status_code, expected_detail",
    [
        (
            {},
            422,
            {
                "detail": [
                    {
                        "type": "missing",
                        "loc": ["body", "tg_id"],
                        "msg": "Field required",
                        "input": {},
                        "url": "https://errors.pydantic.dev/2.4/v/missing",
                    },
                    {
                        "type": "missing",
                        "loc": ["body", "phone_number"],
                        "msg": "Field required",
                        "input": {},
                        "url": "https://errors.pydantic.dev/2.4/v/missing",
                    },
                    {
                        "type": "missing",
                        "loc": ["body", "tg_nickname"],
                        "msg": "Field required",
                        "input": {},
                        "url": "https://errors.pydantic.dev/2.4/v/missing",
                    },
                    {
                        "type": "missing",
                        "loc": ["body", "verification_code"],
                        "msg": "Field required",
                        "input": {},
                        "url": "https://errors.pydantic.dev/2.4/v/missing",
                    },
                    {
                        "type": "missing",
                        "loc": ["body", "registration_time"],
                        "msg": "Field required",
                        "input": {},
                        "url": "https://errors.pydantic.dev/2.4/v/missing",
                    },
                ]
            },
        ),
        (
            {
                "tg_id": "88005553535",
                "phone_number": "9232453434",
                "tg_nickname": "pogchamp",
                "verification_code": 123456,
                "registration_time": datetime.strftime(
                    datetime.now(UTC), "%Y-%m-%d %H:%M:%S"
                ),
            },
            422,
            {
                "detail": "Phone number should start with +7 and contain only digits after that"
            },
        ),
        (
            {
                "tg_id": "88005553535",
                "phone_number": "+7880055535353232",
                "tg_nickname": "pogchamp",
                "verification_code": 123456,
                "registration_time": datetime.strftime(
                    datetime.now(UTC), "%Y-%m-%d %H:%M:%S"
                ),
            },
            422,
            {"detail": "Phone number should contain exactly 12 symbols"},
        ),
    ],
)
async def test_create_user_validation_error(
    client, user_data_for_creation, expected_status_code, expected_detail
):
    resp = client.post("/user/create", content=json.dumps(user_data_for_creation))
    data_from_resp = resp.json()
    assert resp.status_code == expected_status_code
    assert data_from_resp == expected_detail


async def test_create_user_with_wrong_verification_code(client, add_user_to_redis):
    user_data = {
        "tg_id": "88005553535",
        "phone_number": "+79991234567",
        "tg_nickname": "pogchamp",
        "verification_code": 654321,
        "registration_time": datetime.strftime(datetime.now(UTC), "%Y-%m-%d %H:%M:%S"),
    }
    await add_user_to_redis(
        user_data["tg_id"], user_data["phone_number"], user_data["tg_nickname"], 123456
    )
    resp = client.post("/user/create", content=json.dumps(user_data))
    assert resp.status_code == 422
    assert "Wrong verification code" in resp.json()["detail"]


async def test_create_user_with_expired_code(client, add_user_to_redis):
    user_data = {
        "tg_id": "88005553535",
        "phone_number": "+79991234567",
        "tg_nickname": "pogchamp",
        "verification_code": 123456,
        "registration_time": datetime.strftime(
            datetime.now(UTC) + timedelta(minutes=30), "%Y-%m-%d %H:%M:%S"
        ),
    }
    await add_user_to_redis(
        user_data["tg_id"], user_data["phone_number"], user_data["tg_nickname"], 123456
    )
    resp = client.post("/user/create", content=json.dumps(user_data))
    assert resp.status_code == 422
    assert "The code has expired. Request new code" in resp.json()["detail"]
