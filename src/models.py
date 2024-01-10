import uuid
from datetime import datetime

from redis.commands.search.field import NumericField, TextField
from sqlalchemy import String, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    tg_id: Mapped[str] = mapped_column(unique=True)
    phone_number: Mapped[str] = mapped_column(String(12), unique=True)
    tg_nickname: Mapped[str] = mapped_column(String(32), nullable=False)
    registration_date: Mapped[datetime] = mapped_column(server_default=func.now())
    last_login_date: Mapped[datetime] = mapped_column(server_default=func.now())

    def __repr__(self) -> str:
        return f"User(id={self.id}, phone_number={self.phone_number})"


redis_schema = (
    TextField("$.tg_id", as_name="tg_id"),
    TextField("$.phone_number", as_name="phone_number"),
    NumericField("$.verification_code", as_name="code"),
    TextField("$.expire_at", as_name="expire_at"),
)
