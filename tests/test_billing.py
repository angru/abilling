from datetime import datetime
from decimal import Decimal

import pytest
import sqlalchemy as sa

from abilling import models
from abilling.app.db import Db
from abilling.billing import Billing
from abilling.utils import errors
from abilling.utils.constants import OperationType
from tests.conftest import TestWithDb
from tests.utils import EqMock

pytestmark = pytest.mark.asyncio


async def get_transactions(wallet_id: int, db: Db):
    async with db.connection() as connection:
        transactions = await connection.fetch(
            sa.select([models.transaction]).where(wallet_id == wallet_id),
        )

    return [dict(t) for t in transactions]


class TestBilling(TestWithDb):
    @pytest.fixture
    async def client(self, db: Db):
        async with db.executor(Billing) as executor:
            client = await executor.create_client('Bill')
            wallet = await executor.create_wallet(client['id'])

        client['wallet'] = wallet

        return client

    async def test_create_client(self, db: Db):
        async with db.transaction() as t:
            client = await Billing(t).create_client('Bill')

        assert client == {
            'id': EqMock(int),
            'name': 'Bill',
            'date': EqMock(datetime),
        }

    async def test_get_client(self, client, db: Db):
        async with db.connection() as connection:
            found_client = await Billing(connection).get_client(client['id'])

        assert found_client == client
        assert found_client is not client

    async def test_get_client_not_found(self, db: Db):
        async with db.connection() as connection:
            with pytest.raises(errors.NotFound):
                await Billing(connection).get_client(1)

    async def test_create_wallet(self, db: Db):
        async with db.executor(Billing) as executor:
            client = await executor.create_client('Bill')
            wallet = await executor.create_wallet(client['id'])

        assert wallet == {
            'id': EqMock(int),
            'balance': Decimal('0'),
        }

    async def test_create_wallet_client_not_found(self, db: Db):
        async with db.connection() as connection:
            with pytest.raises(errors.NotFound):
                await Billing(connection).create_wallet(client_id=1)

    async def test_create_wallet_with_wrong_currency(self, db: Db):
        async with db.connection() as connection:
            with pytest.raises(ValueError):
                await Billing(connection).create_wallet(1, 'RUB')

    async def test_make_transaction_wallet_not_found(self, db: Db):
        async with db.connection() as connection:
            with pytest.raises(errors.NotFound):
                await Billing(connection).save_transaction(1, Decimal('1'), OperationType.ACCRUAL)

    async def test_make_transaction(self, client: dict, db: Db):
        wallet_id = client['wallet']['id']

        transactions = await get_transactions(wallet_id, db)

        assert transactions == []

        async with db.connection() as connection:
            await Billing(connection).save_transaction(
                wallet_id, Decimal('1'), OperationType.ACCRUAL,
                description={'wallet_from': 2},
            )

        transactions = await get_transactions(wallet_id, db)

        assert transactions == [
            {
                'id': EqMock(int),
                'date': EqMock(datetime),
                'type': OperationType.ACCRUAL,
                'wallet_id': wallet_id,
                'amount': Decimal('1'),
                'description': '{"wallet_from": 2}',  # BUG: https://github.com/CanopyTax/asyncpgsa/issues/44
            },
        ]

    async def test_change_balance_wallet_not_found(self, db: Db):
        async with db.connection() as connection:
            with pytest.raises(errors.NotFound):
                await Billing(connection).change_balance(1, Decimal('1'))

    async def test_change_balance_not_enough_money(self, client: dict, db: Db):
        async with db.connection() as connection:
            with pytest.raises(errors.NotEnoughMoney):
                await Billing(connection).change_balance(client['wallet']['id'], -Decimal('1'))
