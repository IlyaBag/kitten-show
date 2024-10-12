import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_breeds(ac_fxt: AsyncClient):
    response = await ac_fxt.get('/api/v1/breeds')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "id": 1,
            "name": "Chantilly-Tiffany"
        },
        {
            "id": 2,
            "name": "Siamese"
        },
        {
            "id": 3,
            "name": "Exotic Shorthair"
        }
    ]

@pytest.mark.asyncio
async def test_create_kitten(ac_fxt: AsyncClient, kitten_payload_fxt):
    response = await ac_fxt.post('/api/v1/kittens', json=kitten_payload_fxt)
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.asyncio
async def test_get_kittens(ac_fxt: AsyncClient):
    response = await ac_fxt.get('/api/v1/kittens')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            'color': 'Gray',
            'age': 2,
            'description': 'Our first kitten',
            'id': 1,
            'breed': {
                'id': 1,
                'name': 'Chantilly-Tiffany'
            }
        },
        {
            'color': 'White',
            'age': 3,
            'description': 'Pretty nice kitten',
            'id': 2,
            'breed': {
                'id': 2,
                'name': 'Siamese'
            }
        }
    ]

@pytest.mark.asyncio
async def test_get_kittens_filter_breed(ac_fxt: AsyncClient):
    response = await ac_fxt.get('/api/v1/kittens',
                                params={'filter_breed_id': 2})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            'color': 'White',
            'age': 3,
            'description': 'Pretty nice kitten',
            'id': 2,
            'breed': {
                'id': 2,
                'name': 'Siamese'
            }
        }
    ]

@pytest.mark.asyncio
async def test_get_kitten(ac_fxt: AsyncClient):
    response = await ac_fxt.get('/api/v1/kittens/2')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'color': 'White',
        'age': 3,
        'description': 'Pretty nice kitten',
        'id': 2,
        'breed': {
            'id': 2,
            'name': 'Siamese'
        }
    }

@pytest.mark.asyncio
async def test_update_kitten(ac_fxt: AsyncClient, kitten_payload_updated_fxt):
    response = await ac_fxt.patch('/api/v1/kittens/2',
                                  json=kitten_payload_updated_fxt)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['details'] == 'Updated successfully'

    response = await ac_fxt.get('/api/v1/kittens/2')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'color': 'White',
        'age': 10,
        'description': 'Very nice kitten',
        'id': 2,
        'breed': {
            'id': 1,
            'name': 'Chantilly-Tiffany'
        }
    }

@pytest.mark.asyncio
async def test_delete_kitten(ac_fxt: AsyncClient):
    response = await ac_fxt.delete('/api/v1/kittens/2')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['details'] == 'Deleted successfully'
