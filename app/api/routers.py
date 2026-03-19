from fastapi import APIRouter

from app.api.endpoints.short_link import router as short_link_router


main_router = APIRouter()

main_router.include_router(
    short_link_router,
    tags=['Короткая ссылка'],
)
