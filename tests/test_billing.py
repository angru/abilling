from decimal import Decimal

import pytest

from abilling.api import controllers
from abilling.app.db import Db
from tests.conftest import TestWithDb
from tests.utils import EqMock

pytestmark = pytest.mark.asyncio


class TestBilling(TestWithDb):
    async def test_create_client(self, db: Db):
        client = await controllers.create_client(name='Bill', db=db)

        client_id = EqMock(store_value=True, type=int)

        assert client == {
            'id': client_id,
            'date': EqMock(),
            'name': 'Bill',
            'wallet': {
                'id': EqMock(),
                'client_id': client_id,
                'balance': Decimal(0),
            },
        }

    async def test_charge(self, db: Db):
        client = await controllers.create_client(name='Bill', db=db)

        await controllers.charge_wallet(client['id'], Decimal(10), db)

    async def test_transfer(self, db: Db):
        client1 = await controllers.create_client(name='Bill', db=db)
        client2 = await controllers.create_client(name='John', db=db)

        await controllers.charge_wallet(client1['id'], Decimal(10), db)
        await controllers.make_transfer(client1['id'], client2['id'], Decimal(10), db)
