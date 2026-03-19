from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column


from app.core import constants
from app.core.db import Base, TimestampedMixin


class ShortLink(Base, TimestampedMixin):
    """Модель для короткой ссылки."""

    url: Mapped[str] = mapped_column(String(), unique=True)
    short_id: Mapped[str] = mapped_column(
        String(constants.MAX_LEN_SHORT_LINK), index=True, unique=True
    )
    click_link: Mapped[int] = mapped_column(Integer, default=0)

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}('
            f'url={self.url} '
            f'short_id={self.short_id}, '
            f'click_count={self.click_link}'
        )
