from pydantic import BaseModel, HttpUrl


class CreateShortLinkSchema(BaseModel):
    """Схема для создания короткой ссылки."""
    url: HttpUrl


class GetShortLinkSchema(BaseModel):
    """Схема для получения короткой ссылки."""
    short_id: str


class GetClickCountSchema(BaseModel):
    """Схема для получения колличества переходов по короткой ссылки."""
    click_link: int
