import os
import sys
from typing import AsyncGenerator

sys.path.insert(1, os.path.dirname(sys.path[0]))

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.pool import NullPool

from config import DB_ECHO, DB_HOST, DB_PASS, DB_PORT, DB_USER
from database.helpers import get_db_session
from database.models import Base, BreedModel, KittenModel
from main import app


TEST_DB_URL = (
    f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/test_db'
)

test_engine = create_async_engine(TEST_DB_URL, echo=DB_ECHO, poolclass=NullPool)
test_async_session_factory = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def override_get_db_session() -> AsyncGenerator[AsyncSession, None]:
    # session = test_async_session_factory()
    # try:
    #     yield session
    # finally:
    #     await session.close()
    async with test_async_session_factory() as session:
        yield session

app.dependency_overrides[get_db_session] = override_get_db_session

async def populate_db():
    '''Populate the database with some initial data.'''
    async with test_engine.begin() as conn:
        stmt = insert(BreedModel).values([
            {'name': 'Chantilly-Tiffany'},
            {'name': 'Siamese'},
            {'name': 'Exotic Shorthair'}
        ])
        await conn.execute(stmt)
        stmt = insert(KittenModel).values({
            'color': 'Gray',
            'age': 2,
            'description': 'Our first kitten',
            'breed_id': 1
        })
        await conn.execute(stmt)

@pytest_asyncio.fixture(autouse=True, scope='session')
async def prepare_database_fxt():
    '''Create and populate the database before testing ans drop it after.'''
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await populate_db()
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# @pytest_asyncio.fixture(scope='session')
# def event_loop_fxt(request):
#     """Create an instance of the default event loop for each test case."""
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()

@pytest_asyncio.fixture(scope='session')
async def ac_fxt() -> AsyncGenerator[AsyncClient, None]:
    '''Spawn an async client to interact with an API app.'''
    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url='http://127.0.0.1:8000/') as ac:
        yield ac

@pytest.fixture
def kitten_payload_fxt():
    '''Generate a kitten payload.'''
    return {
        'color': 'White',
        'age': 3,
        'description': 'Pretty nice kitten',
        'breed_id': 2
    }

@pytest.fixture
def kitten_payload_updated_fxt():
    '''Generate an updated kitten payload.'''
    return {
        'color': 'White',
        'age': 10,
        'description': 'Very nice kitten',
        'breed_id': 1
    }
