import asyncio
from decimal import Decimal

import pytest

from abilling import controllers
from abilling.config import config
from abilling.db import Storage

pytestmark = pytest.mark.asyncio

class EqMock:
    value = ...

    def __init__(self, store_value=False):
        self.store_value = store_value

    def __repr__(self):
        if self.value:
            return 'Not compared yet'

        return str(self.value)

    def __eq__(self, other):
        if self.store_value:
            if self.value is ...:
                self.value = other
        else:
            self.value = other

        return self.value == other


async def test_create_client():
    storage = Storage(config.DB_PG_URL)

    await storage.init()

    client = await controllers.create_client(name='Bill', storage=storage)

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