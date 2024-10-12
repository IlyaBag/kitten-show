import pytest
from fastapi import HTTPException, status

from conftest import test_async_session_factory as session_maker
from database.helpers import get_kitten_by_id


@pytest.mark.asyncio
async def test_get_kitten_by_id():
    '''Check the function that getting a kitten ORM model from a database
    by id.'''
    async with session_maker() as session:
        kitten_orm = await get_kitten_by_id(id=1, session=session)
        kitten = {
            'color': kitten_orm.color,
            'age': kitten_orm.age,
            'description': kitten_orm.description,
            'breed_id': kitten_orm.breed_id
        }
    assert kitten == {
            'color': 'Gray',
            'age': 2,
            'description': 'Our first kitten',
            'breed_id': 1
        }

@pytest.mark.asyncio
async def test_get_kitten_by_wrong_id():
    '''Check exception handling when trying to get a kitten ORM model from
    a database with a non-existent id.'''
    with pytest.raises(HTTPException):
        async with session_maker() as session:
            response_exc = await get_kitten_by_id(id=9, session=session)
        assert response_exc.status_code == status.HTTP_404_NOT_FOUND
        assert response_exc.detail == (
            'Sorry, but the kitten with id=9 was not found'
        )
