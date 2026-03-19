"""Общие константы."""

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE_PATH = BASE_DIR / 'infra' / '.env'

# short_link
MAX_LEN_SHORT_LINK = 20
ATTEMPTS_CREATE_SHORT_LINK = 100

# Логrер
LOG_DIR = BASE_DIR / 'app' / 'logs'
LOG_FILE = LOG_DIR / 'app.log'
LOG_FORMAT = '%(asctime)s - [%(levelname)s] - %(message)s'
DT_FORMAT = '%d.%m.%Y %H:%M:%S'
MAX_BYTES = 10**6
BACKUP_COUNT = 5
ENCODING = 'utf-8'
