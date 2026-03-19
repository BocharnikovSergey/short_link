import secrets

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exists, select

from app.core import constants
from app.core.logger import logger_event as logger
from app.models.short_link import ShortLink


async def create_short_link(
    session: AsyncSession,
    model: type[ShortLink],
    max_length: int = constants.MAX_LEN_SHORT_LINK
) -> str:
    """Создание короткой ссылки."""
    logger.info('Начало создания короткой ссылки.')
    for _ in range(constants.ATTEMPTS_CREATE_SHORT_LINK):
        short_id = secrets.token_urlsafe(max_length)[:max_length]
        if not (await session.execute(select(
            exists().where(model.short_id == short_id)
        ))).scalar():
            break
    else:
        message = 'Не удалось создать короткую ссылку.'
        logger.error(message)
        raise RuntimeError(message)
    return short_id
