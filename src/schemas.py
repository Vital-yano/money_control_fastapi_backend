import re
import uuid
from datetime import datetime

from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, field_validator

PHONE_NUMBER_MATCH_PATTERN = re.compile(r"^\+7[0-9]+$")

VERIFICATION_CODE_MATCH_PATTERN = re.compile(r"^[0-9]{4}$")


def _validate_phone_number(value):
    if not PHONE_NUMBER_MATCH_PATTERN.match(value):
        raise HTTPException(
            status_code=422,
            detail="Phone number should start with +7 and contain only digits after that",
        )
    if len(value) != 12:
        raise HTTPException(
            status_code=422, detail="Phone number should contain exactly 12 symbols"
        )
    return value


class UserCreateSchema(BaseModel):
    tg_id: str
    phone_number: str
    tg_nickname: str
    verification_code: str
    registration_time: datetime

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value):
        return _validate_phone_number(value)

    @field_validator("verification_code")
    @classmethod
    def validate_code(cls, value):
        if not VERIFICATION_CODE_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Code should contain exactly 4 digits"
            )
        return value


class ShowUserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tg_id: str
    phone_number: str
    tg_nickname: str


class UserAddtoRedisSchema(BaseModel):
    tg_id: str
    phone_number: str
    tg_nickname: str

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value):
        return _validate_phone_number(value)


class SendCodeSchema(BaseModel):
    code: str

    @field_validator("code")
    @classmethod
    def validate_code(cls, value):
        if not VERIFICATION_CODE_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422,
                detail="Verification code should be >0000 and <9999",
            )
        return value
