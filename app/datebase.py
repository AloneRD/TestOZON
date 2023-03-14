import asyncio

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_scoped_session
from sqlalchemy.orm import sessionmaker

from settings import DB_HOST, DB_USER, DB_PASS, DB_NAME, DB_PORT


db_url = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
async_engine = create_async_engine(db_url, echo=True)
async_session_factory = sessionmaker(async_engine, class_=AsyncSession)
AsyncScopedSession = async_scoped_session(async_session_factory, asyncio.current_task)


async def get_session() -> AsyncSession:
    async with AsyncScopedSession() as session:
        yield session
