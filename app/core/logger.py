import logging
from logging.handlers import RotatingFileHandler


from app.core import constants


def configure_logging() -> logging.Logger:
    """Настройка логгирования."""
    constants.LOG_DIR.mkdir(exist_ok=True)

    formatter = logging.Formatter(
        fmt=constants.LOG_FORMAT,
        datefmt=constants.DT_FORMAT,
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    rotating_handler = RotatingFileHandler(
        constants.LOG_FILE,
        maxBytes=constants.MAX_BYTES,
        backupCount=constants.BACKUP_COUNT,
        encoding=constants.ENCODING,
    )
    rotating_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.addHandler(rotating_handler)
    logger.addHandler(console_handler)
    return logger


logger_event = configure_logging()
