from datetime import datetime, timezone


def get_utc_now() -> datetime:
    """Получение текущего времени в UTC."""
    return datetime.now(timezone.utc)
