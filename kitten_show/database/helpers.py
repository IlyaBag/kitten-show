from typing import AsyncGenerator

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import async_session_factory
from database.models import KittenModel


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    session = async_session_factory()
    try:
        yield session
    finally:
        await session.close()

async def get_kitten_by_id(
    id: int,
    session: AsyncSession
) -> KittenModel | HTTPException:
    kitten = await session.get(KittenModel, id)
    if not kitten:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Sorry, but the kitten with id={id} was not found'
        )
    return kitten
