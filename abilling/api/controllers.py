from decimal import Decimal

from abilling.app.db import Db
from abilling.utils.constants import OperationType
from abilling.billing import Billing


async def create_client(name: str, db: Db) -> dict:
    async with db.executor(Billing, transaction=True) as executor:
        client = await executor.create_client(name=name)
        client['wallet'] = await executor.create_wallet(client_id=client['id'])

        return client


async def charge_wallet(wallet_id: int, amount: Decimal, db: Db):
    async with db.executor(Billing, transaction=True) as billing:
        await billing.charge_wallet(wallet_id, amount)
        await billing.save_transaction(wallet_id, amount, OperationType.ACCRUAL)


async def make_transfer(wallet_from, wallet_to, amount: Decimal, db: Db):
    async with db.executor(Billing, transaction=True) as billing:
        await billing.withdraw(wallet_id=wallet_from, amount=amount)
        await billing.save_transaction(
            wallet_id=wallet_from, amount=amount,
            operation_type=OperationType.WRITE_OFF,
        )
        await billing.charge_wallet(wallet_id=wallet_to, amount=amount)
        await billing.save_transaction(
            wallet_id=wallet_to, amount=amount,
            operation_type=OperationType.ACCRUAL,
        )


async def get_client(client_id: int, db: Db) -> dict:
    async with db.executor(Billing) as billing:
        return await billing.get_client(client_id)
