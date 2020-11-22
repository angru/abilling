from decimal import Decimal

import pytest

from abilling.app.db import Db
from abilling.billing import Billing
from abilling.utils import errors
from abilling.utils.constants import OperationType
from tests.conftest import TestWithDb


pytestmark = pytest.mark.asyncio


class TestBilling(TestWithDb):
    async def test_make_transaction_wallet_not_found(self, db: Db):
        async with db.connection() as connection:
            with pytest.raises(errors.NotFound):
                await Billing(connection).save_transaction(999999, Decimal('1'), OperationType.ACCRUAL)

    async def test_changre_balance_wallet_not_found(self, db: Db):
        async with db.connection() as connection:
            with pytest.raises(errors.NotFound):
                await Billing(connection).change_balance(999999, Decimal('1'))

    async def test_create_wallet_client_not_found(self, db: Db):
        async with db.connection() as connection:
            with pytest.raises(errors.NotFound):
                await Billing(connection).create_wallet(client_id=99999)
