from fastapi import APIRouter, status
from fastapi.responses import RedirectResponse

from app.api import validators
from app.crud.short_link import crud_short_link
from app.core.db import SessionDep
from app.core.logger import logger_event as logger
from app.schemas.short_link import (
    CreateShortLinkSchema, GetClickCountSchema, GetShortLinkSchema
)


router = APIRouter()


@router.post(
    '/shorten',
    response_model=GetShortLinkSchema,
    status_code=status.HTTP_201_CREATED,
    summary='Создание короткой ссылки.'
)
async def create_short_link(
    obj: CreateShortLinkSchema,
    session: SessionDep,
):
    """Создание короткой ссылки."""
    logger.info('Создание короткой ссылки.')
    return (
        await crud_short_link.get_by_url(url=obj.url, session=session)
        or await crud_short_link.create(obj=obj, session=session)
    )


@router.get(
    '/{short_id}',
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    summary='Редирект.'
)
async def redirect(
    short_id: str, session: SessionDep,
) -> RedirectResponse:
    logger.info(f'Редирект: {short_id}')
    url = await crud_short_link.get_url(short_id=short_id, session=session)
    validators.validator_field_exists(url)
    return RedirectResponse(url=url)


@router.get(
    '/stats/{short_id}', response_model=GetClickCountSchema,
    summary='Получени количества переходов по короткой ссылки.'
)
async def stats(
    short_id: str, session: SessionDep,
):
    logger.info(
        f'Получение количества переходов по короткой ссылки: {short_id}'
    )
    click_link = await crud_short_link.get_by_short_id(
        short_id=short_id, session=session
    )
    validators.validator_field_exists(click_link)
    return click_link
