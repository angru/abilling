import typing as t
from decimal import Decimal

import sqlalchemy as sa

from abilling import models
from abilling.app.db import Executor
from abilling.constants import OperationType


class Billing(Executor):
    async def create_client(self, name) -> dict:
        result = await self.connection.fetchrow(
            models.client.insert(return_defaults=True).values({'name': name}),
        )

        return {
            'id': result['id'],
            'name': name,
            'date': result['date'],
        }

    async def create_wallet(self, client_id) -> dict:
        result = await self.connection.fetchrow(
            sa.insert(models.wallet, return_defaults=True).values(client_id=client_id),
        )

        return {
            'id': result['id'],
            'client_id': client_id,
            'balance': result['balance'],
        }

    async def charge_wallet(self, wallet_id, amount) -> t.NoReturn:
        await self.connection.fetchval(
            sa.update(models.wallet).where(
                models.wallet.c.id == wallet_id
            ).values(balance=models.wallet.c.balance + amount)
        )

    async def get_balance(self, wallet_id) -> Decimal:
        return await self.connection.fetchval(
            sa.select([models.wallet.c.balance]).where(models.wallet.c.id == wallet_id)
        )

    async def save_history(self, wallet_id: int, amount, operation_type: OperationType) -> t.NoReturn:
        await self.connection.fetchval(
            sa.insert(models.operation_history).values(
                wallet_id=wallet_id,
                amount=amount,
                type=operation_type,
            )
        )

    async def withdraw(self, wallet_id, amount):
        balance = await self.connection.fetchval(
            sa.select([models.wallet.c.balance]).with_for_update().where(
                models.wallet.c.id == wallet_id,
            )
        )

        if balance < amount:
            raise ValueError('Not enough money')

        await self.charge_wallet(wallet_id, -amount)  # FIXME: use own query
