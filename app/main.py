from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings
from app.core.logger import configure_logging

configure_logging()

app = FastAPI(
    title=settings.app_title,
)

app.include_router(main_router)
