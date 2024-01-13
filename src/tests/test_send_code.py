import json


async def test_send_code(client, get_user_from_redis):
    user_data = {
        "tg_id": "88005553535",
        "phone_number": "+79991234567",
        "tg_nickname": "pogchamp",
    }
    response = client.post("/user/send_code", content=json.dumps(user_data))
    assert response.status_code == 200
    data_from_resp = response.json()
    redis_user_data = await get_user_from_redis(user_data["tg_id"])
    assert data_from_resp["code"] == 123456
    assert user_data["tg_id"] == redis_user_data["tg_id"]
    assert user_data["phone_number"] == redis_user_data["phone_number"]
    assert user_data["tg_nickname"] == redis_user_data["tg_nickname"]
    assert data_from_resp["code"] == redis_user_data["verification_code"]


async def test_send_code_to_incorrect_phone_number(client):
    phone_number = {"phone_number": "+799912345674343"}
    response = client.post("/user/send_code", content=json.dumps(phone_number))
    assert "Phone number should contain exactly 12 symbols" in response.json()["detail"]
