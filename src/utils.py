import logging
from typing import Protocol

import httpx
from fastapi import HTTPException

logger = logging.getLogger(__name__)


def get_code():
    """Функция нужна для того, чтобы переопределять отправку кода во время тестов"""
    return None


class SendCodeProtocol(Protocol):
    async def send_code(self):
        ...


class SendCodeViaCallProtocol(SendCodeProtocol):
    def __init__(self, url: str):
        self.url = url

    async def send_code(self):
        async with httpx.AsyncClient() as httpx_client:
            response = await httpx_client.get(self.url)
        if response.json().get("status", None) == "OK":
            return str(response.json()["code"])
        else:
            logger.error("Send code service error")
            raise HTTPException(
                status_code=503,
                detail="Проблемы с сервисом отправки смс. Попробуйте зарегистрироваться позже",
            )
