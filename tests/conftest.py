import pytest
import asyncio
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.database import Base, get_test_async_session, test_engine, get_async_session


@pytest.fixture(scope="session")
def event_loop():
    loop=asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()

@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()

@pytest_asyncio.fixture
async def client():
    async def override_get_db():
        async for session in get_test_async_session():
            yield session
    app.dependency_overrides[get_async_session]=override_get_db
    transport = ASGITransport(app=app) 
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def test_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_test_async_session():
        yield session
