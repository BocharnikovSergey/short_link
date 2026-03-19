from typing import Any

from fastapi import HTTPException, status

from app.core.logger import logger_event as logger


def validator_field_exists(field: Any) -> None:
    """Проверяет, что поле не является None."""
    if field is None:
        detail = 'Короткая ссылка не найдена.'
        logger.error(detail)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )
