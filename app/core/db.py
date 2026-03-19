from datetime import datetime
from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy import DateTime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
)
from sqlalchemy.sql import text

from app.core.config import settings
from app.core.logger import logger_event as logger
from app.services.datetimes import get_utc_now

engine = create_async_engine(settings.database_url)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    """Базовый класс для моделей SQLAlchemy."""


class TimestampedMixin:
    """Содержит поля временных меток и статус активности."""

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=get_utc_now,
        server_default=text("TIMEZONE('utc', now())"),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=get_utc_now,
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=get_utc_now,
        server_onupdate=text("TIMEZONE('utc', now())"),
    )

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}('
            f'id={self.id}, '
            f'created_at={self.created_at}, '
            f'updated_at={self.updated_at})'
        )


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Получение асинхронной сессии."""
    try:
        async with AsyncSessionLocal() as async_session:
            yield async_session
    except SQLAlchemyError as error:
        logger.error(f'Ошибка базы данных | {str(error)}')
        await async_session.rollback()
        raise error


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
