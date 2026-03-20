import uuid

import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app as app
from app.core.db import Base, get_async_session as get_async_session


TEST_DATABASE_URL = 'sqlite+aiosqlite:///:memory:'


@pytest_asyncio.fixture(scope='session')
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest_asyncio.fixture(scope='session')
async def async_sessionmaker(test_engine):
    return sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )


@pytest_asyncio.fixture(scope='session')
async def app_test(async_sessionmaker):
    async def _get_async_session():
        async with async_sessionmaker() as session:
            try:
                yield session
            finally:
                await session.rollback()

    app.dependency_overrides[get_async_session] = _get_async_session
    yield app
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client(app_test: FastAPI):
    transport = ASGITransport(app=app_test)
    async with AsyncClient(
        transport=transport, base_url='http://testserver'
    ) as client:
        yield client


@pytest_asyncio.fixture
async def url():
    return f'https://example.com/{uuid.uuid4()}'


@pytest_asyncio.fixture
async def short_id(client, url):

    response = await client.post(
        '/shorten',
        json={'url': url}
    )
    return response.json()['short_id']
