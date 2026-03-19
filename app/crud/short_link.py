from fastapi import HTTPException, status
from pydantic import HttpUrl
from sqlalchemy import select, update, exists
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import logger_event as logger
from app.schemas.short_link import CreateShortLinkSchema
from app.services.utils import create_short_link
from app.models.short_link import ShortLink


class CRUDShortLink:
    """Класс для CRUD операций коротких ссылок."""

    def __init__(self, model: type[ShortLink]) -> None:
        """Инициализация класса."""
        self.model = model

    async def get_by_url(
        self, url: HttpUrl, session: AsyncSession
    ) -> type[ShortLink] | None:
        """Получение короткой ссылки по оригинальному URL."""
        logger.info('fПоиск короткой ссылки для URL: {url}')
        return (
                await session.execute(
                    select(self.model).where(
                        self.model.url == str(url)
                    )
                )).scalars().first()

    async def get_url(
        self, short_id: str, session: AsyncSession
    ) -> str | None:
        """
        Получение оригинального URL по short_id
        с одновременным увеличением счётчика переходов.
        """
        logger.info(
            f'Запрос оригинального URL для short_id: {short_id}. '
            f'Увеличение счётчика кликов.'
        )
        if url := (await session.execute(
            update(self.model)
            .where(self.model.short_id == short_id)
            .values(click_link=self.model.click_link + 1)
            .returning(self.model.url)

        )).scalars().first():
            await session.commit()
        else:
            logger.warning('Ссылка не найдена.')
            await session.rollback()
        return url

    async def get_by_short_id(
        self, short_id: str, session: AsyncSession
    ) -> type[ShortLink] | None:
        """Получение короткой ссылки по short_id."""
        logger.info(f'Поиск короткой ссылки по short_id: {short_id}')
        return (
                await session.execute(
                    select(self.model).where(
                        self.model.short_id == short_id
                    )
                )
            ).scalars().first()

    async def create(
        self,
        obj: CreateShortLinkSchema,
        session: AsyncSession,
    ) -> type[ShortLink]:
        """Метод для добавления записи в базу."""
        logger.info('Создания записи в БД.')
        try:
            short_id = await create_short_link(
                session=session, model=self.model
            )
            data = obj.model_dump(mode='json')
            data['short_id'] = short_id
            db_obj = self.model(**data)
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj
        except IntegrityError as error:
            logger.error(error)
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=error
            )


crud_short_link = CRUDShortLink(model=ShortLink)
