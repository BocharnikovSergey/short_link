from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.constants import ENV_FILE_PATH


class Settings(BaseSettings):
    """Настройки проекта."""

    app_title: str = 'Создание коротких ссылок.'
    postgres_user: str
    postgres_password: str
    postgres_host: str = 'localhost'
    postgres_port: str = '5432'
    postgres_db: str = 'db'
    secret: str
    algorithm: str = 'HS256'

    model_config = SettingsConfigDict(env_file=str(ENV_FILE_PATH))

    @property
    def database_url(self) -> str:
        """Собирает URL для подключения к базе данных."""
        return (
            'postgresql+asyncpg://'
            f'{self.postgres_user}:{self.postgres_password}'
            f'@{self.postgres_host}:{self.postgres_port}/'
            f'{self.postgres_db}'
        )


settings = Settings()
