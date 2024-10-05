from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from api_v1.schemas import Breed, CreateKitten, Kitten, UpdateKitten
from database.helpers import get_db_session, get_kitten_by_id
from database.models import BreedModel, KittenModel


router = APIRouter(tags=['Kittens'])


@router.get('/breeds', response_model=list[Breed])
async def get_breeds(session: AsyncSession = Depends(get_db_session)):
    '''Returns a list of all breeds'''
    stmt = select(BreedModel)
    result: Result = await session.execute(stmt)
    return result.scalars().all()


@router.get('/kittens', response_model=list[Kitten])
async def get_kittens(
    filter_breed_id: Annotated[int | None, Query()] = None,
    session: AsyncSession = Depends(get_db_session)
):
    '''Returns a list of all kittens with their breed. Allows you to filter
    kittens by their breed using the "filter_breed_id" query parameter.'''
    stmt = select(KittenModel).options(joinedload(KittenModel.breed))
    if filter_breed_id:
        stmt = stmt.filter(KittenModel.breed_id==filter_breed_id)
    result: Result = await session.execute(stmt)
    kitten_list = result.scalars().all()
    return kitten_list


@router.get('/kittens/{id}', response_model=Kitten)
async def get_kitten(id: int, session: AsyncSession = Depends(get_db_session)):
    '''Returns all information about the kitten with id = "id"'''
    stmt = (select(KittenModel)
            .filter(KittenModel.id==id)
            .options(joinedload(KittenModel.breed)))
    result: Result = await session.execute(stmt)
    kitten = result.scalar()
    if not kitten:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Sorry, but the kitten with id={id} was not found'
        )
    return kitten


@router.post('/kittens', status_code=status.HTTP_201_CREATED)
async def add_kitten(
    params: CreateKitten,
    session: AsyncSession = Depends(get_db_session),
):
    '''Creates a new kitten'''
    new_kitten = KittenModel(**params.model_dump())
    session.add(new_kitten)
    await session.commit()


@router.patch('/kittens/{id}')
async def update_kitten(
    id: int,
    params: UpdateKitten,
    session: AsyncSession = Depends(get_db_session),
):
    '''Updates information about the kitten with id = "id"'''
    kitten = await get_kitten_by_id(id, session)
    for key, val in params.model_dump(exclude_none=True).items():
        kitten.__setattr__(key, val)
    await session.commit()
    return {'details': 'Updated successfully'}


@router.delete('/kittens/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_kitten(id: int, session: AsyncSession = Depends(get_db_session)):
    '''Deletes the kitten with id = "id"'''
    kitten = await get_kitten_by_id(id, session)
    await session.delete(kitten)
    await session.commit()
    return {'details': 'Deleted successfully'}
