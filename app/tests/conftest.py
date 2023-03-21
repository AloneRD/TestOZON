import asyncio

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy_utils.functions import database_exists, create_database


from main import create_app
from settings import DB_HOST, DB_USER, DB_PASS, DB_NAME, DB_PORT
from app.models.__meta__ import Base
from app.datebase import get_session


DATABASE_URL_TEST = f"{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/test_{DB_NAME}"

if not database_exists(f"postgresql://{DATABASE_URL_TEST}"):
    create_database(f"postgresql://{DATABASE_URL_TEST}")

engine_test = create_async_engine(f'postgresql+asyncpg://{DATABASE_URL_TEST}', poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession)
Base.metadata.bind = engine_test


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

async def override_get_session():
    async with async_session_maker() as session:
        yield session

app = create_app()
app.dependency_overrides[get_session] = override_get_session

@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client