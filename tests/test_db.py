from decimal import Decimal

import pytest

from abilling.api import controllers
from abilling.app.config import config
from abilling.app.db import Db
from abilling.billing import Billing
from tests.utils import EqMock

pytestmark = pytest.mark.asyncio


async def test_create_client():
    db = Db(config.DB_PG_URL)
    await db.init()

    client = await controllers.create_client(name='Bill', db=db)

    client_id = EqMock(store_value=True)

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

    await db.stop()


async def test_charge():
    db = Db(config.DB_PG_URL)
    await db.init()
    await controllers.charge_wallet(1, Decimal(10), db)
    await db.stop()


async def test_transfer():
    db = Db(config.DB_PG_URL)
    await db.init()
    await controllers.make_transfer(1, 2, 20, db)
    await db.stop()
