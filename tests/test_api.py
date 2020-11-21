from decimal import Decimal

import pytest
from async_asgi_testclient import TestClient
from async_asgi_testclient.response import Response

from abilling.app.fastapi import create_app
from abilling.utils import errors
from tests.conftest import TestWithDb
from tests.utils import EqMock


pytestmark = pytest.mark.asyncio


@pytest.fixture
async def client():
    async with TestClient(application=create_app()) as client:
        yield client


async def test_docs(client: TestClient):
    response: Response = await client.get('/docs')

    assert response.status_code == 200


class TestApi(TestWithDb):
    async def test_create_client(self, client: TestClient):
        response: Response = await client.post('/clients', json={'name': 'Bob'})

        assert response.status_code == 201, response.text
        assert response.json() == {
            'id': EqMock(),
            'name': 'Bob',
            'wallet': {
                'id': EqMock(),
                'balance': '0',
            },
        }

    async def test_get_client(self, client: TestClient):
        response: Response = await client.post('/clients', json={'name': 'Tom'})

        assert response.status_code == 201, response.text

        client_id = response.json()['id']

        response: Response = await client.get(f'/clients/{client_id}')

        assert response.status_code == 200, response.text
        assert response.json() == {
            'id': EqMock(),
            'name': 'Tom',
            'wallet': {
                'id': EqMock(),
                'balance': '0',
            },
        }

    async def test_charge_wallet(self, client: TestClient):
        response: Response = await client.post('/clients', json={'name': 'Tom'})

        assert response.status_code == 201, response.text

        client_id = response.json()['id']
        wallet_id = response.json()['wallet']['id']

        response: Response = await client.post('/charges', json={'wallet_id': wallet_id, 'amount': '10.999'})

        assert response.status_code == 204, response.text

        response: Response = await client.get(f'/clients/{client_id}')

        assert response.json()['wallet']['balance'] == '10.999'

    async def test_transfer_when_penniless(self, client: TestClient):
        response: Response = await client.post('/clients', json={'name': 'Tom'})
        client1_id = response.json()['id']
        wallet1_id = response.json()['wallet']['id']

        response: Response = await client.post('/clients', json={'name': 'Helen'})
        client2_id = response.json()['id']
        wallet2_id = response.json()['wallet']['id']

        response: Response = await client.post(
            path='/charges',
            json={'wallet_id': wallet1_id, 'amount': '5'},
        )

        assert response.status_code == 204

        response: Response = await client.post(
            path='/transfers',
            json={'wallet_from': wallet1_id, 'wallet_to': wallet2_id, 'amount': '10'},
        )

        assert response.status_code == 400
        assert response.json() == {
            'error': 'NOT_ENOUGH_MONEY', 'message': EqMock(), 'detail': None,
        }

        response: Response = await client.get(f'/clients/{client1_id}')

        assert response.json()['wallet']['balance'] == '5'

        response: Response = await client.get(f'/clients/{client2_id}')

        assert response.json()['wallet']['balance'] == '0'

    async def test_transfer(self, client: TestClient):
        response: Response = await client.post('/clients', json={'name': 'Tom'})
        client1_id = response.json()['id']
        wallet1_id = response.json()['wallet']['id']

        response: Response = await client.post('/clients', json={'name': 'Helen'})
        client2_id = response.json()['id']
        wallet2_id = response.json()['wallet']['id']

        response: Response = await client.post(
            path='/charges',
            json={'wallet_id': wallet1_id, 'amount': '5'},
        )

        assert response.status_code == 204

        response: Response = await client.post(
            path='/transfers',
            json={'wallet_from': wallet1_id, 'wallet_to': wallet2_id, 'amount': '2.9997'},
        )

        assert response.status_code == 204

        response: Response = await client.get(f'/clients/{client1_id}')

        assert response.json()['wallet']['balance'] == '2.0003'

        response: Response = await client.get(f'/clients/{client2_id}')

        assert response.json()['wallet']['balance'] == '2.9997'



