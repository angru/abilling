from decimal import Decimal

import pytest
import sqlalchemy as sa

from abilling import models
from abilling.api import controllers
from abilling.app.db import Db
from abilling.utils import errors
from tests.conftest import TestWithDb
from tests.utils import EqMock

pytestmark = pytest.mark.asyncio


async def get_balance(wallet_id, db: Db):
    async with db.connection() as connection:
        return await connection.fetchval(
            sa.select([models.wallet.c.balance]).where(
                models.wallet.c.id == wallet_id,
            ),
        )


class TestControllers(TestWithDb):
    async def test_create_client(self, db: Db):
        client = await controllers.create_client(name='Bill', db=db)

        assert client == {
            'id': EqMock(),
            'date': EqMock(),
            'name': 'Bill',
            'wallet': {
                'id': EqMock(),
                'balance': Decimal(0),
            },
        }

    async def test_charge(self, db: Db):
        client = await controllers.create_client(name='Bill', db=db)

        await controllers.charge_wallet(client['wallet']['id'], Decimal(10), db)

        assert await get_balance(client['wallet']['id'], db) == Decimal(10)

    async def test_charge_wallet_not_exists(self, db: Db):
        with pytest.raises(errors.NotFound):
            await controllers.charge_wallet(999999, Decimal(10), db)

    async def test_transfer(self, db: Db):
        client1 = await controllers.create_client(name='Bill', db=db)
        client2 = await controllers.create_client(name='John', db=db)

        await controllers.charge_wallet(client1['wallet']['id'], Decimal('10'), db)
        await controllers.make_transfer(
            client1['wallet']['id'], client2['wallet']['id'], Decimal('5.5555'), db,
        )

        assert await get_balance(client1['wallet']['id'], db) == Decimal('4.4445')
        assert await get_balance(client2['wallet']['id'], db) == Decimal('5.5555')

    async def test_get_client(self, db: Db):
        new_client = await controllers.create_client(name='Bill', db=db)
        found_client = await controllers.get_client(new_client['id'], db)

        assert found_client == new_client
        assert found_client is not new_client
