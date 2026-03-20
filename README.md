# short_link
API для сервиса сокращения ссылок (аналог bitly)

### Основной функционал:
- эндпоинт POST /shorten принимает длинную ссылку, возвращает короткий идентификатор
- эндпоинт GET /{short_id} редиректит на оригинальную ссылку
- эндпоинт GET /stats/{short_id} возвращает количество переходов

## Как локально запустить проект:
Пример .env находится в .infra/.env.example
1. Клонировать репозиторий и перейти в него в командной строке:
```bash
git git@github.com:BocharnikovSergey/short_link.git
cd ./short_link
```

2. Cоздать и активировать виртуальное окружение:
Windows
```bash
python -m venv venv
source venv/Scripts/activate
```
Linux/macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Установить зависимости из файла requirements.txt:
```bash
pip install -r app/requirements.txt

```

4. Создание миграций:
```bash
alembic -c ./app/alembic.ini upgrade head
```

5. Запуск приложения для разработки
```bash
uvicorn app.main:app --reload
```

6. Запуск приложения через Docker:
```bash
docker compose -f infra/docker-compose.yml up --build
```

## Запуск тестов.
Из главной директории проекта для запуска тестов нужно выполнить команду.
```bash
pytest
```

## Документация:
[Swagger UI](https://ourdevilcafe.online/docs)\
[ReDoc](https://ourdevilcafe.online/redoc)


## Использованные технологии:
- **Python 3.13** - язык программирования
- **FastAPI** - веб-фреймворк для разработки
- **Postgres** - СУБД для хранения данных
- **SQLAlchemy** - библиотека для работы с СУБД
- **Alembic** - инструмент для управления миграциями
- **Logging** - модуль для логированния
- **Docker** - платформа контейнеризации
