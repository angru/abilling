import typing as t

import sqlalchemy as sa
import asyncpg.exceptions

from abilling import models
from abilling.utils import errors
from abilling.app.db import Executor
from abilling.utils.constants import OperationType


class Billing(Executor):
    async def get_client(self, client_id: int) -> dict:
        result = await self.connection.fetchrow(
            sa.select([
                models.client.c.id,
                models.client.c.name,
                models.client.c.date,
                models.wallet.c.id,
                models.wallet.c.balance,
            ]).select_from(
                models.client.join(models.wallet),
            ).where(
                models.client.c.id == client_id,
            ),
        )

        if not result:
            raise errors.NotFound(message=f'Client with id: {client_id} not found')

        return {
            'id': result[0],
            'name': result[1],
            'date': result[2],
            'wallet': {
                'id': result[3],
                'balance': result[4],
            },
        }

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
        try:
            result = await self.connection.fetchrow(
                sa.insert(models.wallet, return_defaults=True).values(client_id=client_id),
            )
        except asyncpg.exceptions.ForeignKeyViolationError:
            raise errors.NotFound(f'Client with id: {client_id} not found')

        return {
            'id': result['id'],
            'balance': result['balance'],
        }

    async def charge_wallet(self, wallet_id, amount) -> t.NoReturn:
        result = await self.connection.fetchval(
            sa.update(models.wallet).where(
                models.wallet.c.id == wallet_id,
            ).values(
                balance=models.wallet.c.balance + amount,
            ).returning(models.wallet.c.id),
        )

        if not result:
            raise errors.NotFound(f'Wallet with id: {wallet_id} not found')

    async def save_history(self, wallet_id: int, amount, operation_type: OperationType) -> t.NoReturn:
        try:
            await self.connection.fetchval(
                sa.insert(models.operation_history).values(
                    wallet_id=wallet_id,
                    amount=amount,
                    type=operation_type,
                ),
            )
        except asyncpg.exceptions.ForeignKeyViolationError:
            raise errors.NotFound(f'Wallet with id: {wallet_id} not found')

    async def withdraw(self, wallet_id, amount):
        balance = await self.connection.fetchval(
            sa.select([models.wallet.c.balance]).with_for_update().where(
                models.wallet.c.id == wallet_id,
            ),
        )

        if balance is None:
            raise errors.NotFound(f'Wallet with id: {wallet_id} not found')

        if balance < amount:
            raise errors.NotEnoughMoney(message='Not enough money to perform transfer')

        await self.connection.fetchval(
            sa.update(models.wallet).where(
                models.wallet.c.id == wallet_id,
            ).values(balance=models.wallet.c.balance - amount),
        )
