from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, \
create_async_engine

from config import DB_ECHO, DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER


engine = create_async_engine(
    f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}',
    echo=DB_ECHO,
)

async_session_factory = async_sessionmaker(engine, autoflush=False,
                                           expire_on_commit=False)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    session = async_session_factory()
    try:
        yield session
    finally:
        await session.close()
