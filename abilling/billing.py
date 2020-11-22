import typing as t
from decimal import Decimal

import sqlalchemy as sa
import asyncpg.exceptions

from abilling import models
from abilling.utils import errors
from abilling.app.db import Executor
from abilling.utils.constants import OperationType, Currency


class Billing(Executor):
    async def get_client(self, client_id: int) -> dict:
        result = await self.connection.fetchrow(
            sa.select([
                models.client.c.id,
                models.client.c.name,
                models.client.c.date,
                models.wallet.c.id.label('wallet_id'),
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
            'id': result['id'],
            'name': result['name'],
            'date': result['date'],
            'wallet': {
                'id': result['wallet_id'],
                'balance': result['balance'],
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

    async def create_wallet(self, client_id: int, currency: str = Currency.USD) -> dict:
        currency_id = await self.connection.fetchval(
            sa.select([models.currency.c.id]).where(
                models.currency.c.code == currency,
            ),
        )

        try:
            result = await self.connection.fetchrow(
                sa.insert(
                    models.wallet, return_defaults=True,
                ).values(client_id=client_id, currency_id=currency_id),
            )
        except asyncpg.exceptions.ForeignKeyViolationError:
            raise errors.NotFound(f'Client with id: {client_id} not found')

        return {
            'id': result['id'],
            'balance': result['balance'],
        }

    async def change_balance(self, wallet_id: int, amount: Decimal) -> t.NoReturn:
        try:
            result = await self.connection.fetchval(
                sa.update(models.wallet).where(
                    models.wallet.c.id == wallet_id,
                ).values(
                    balance=models.wallet.c.balance + amount,
                ).returning(models.wallet.c.id),
            )
        except asyncpg.exceptions.CheckViolationError:
            raise errors.NotEnoughMoney(message='Not enough money to change balance')

        if not result:
            raise errors.NotFound(f'Wallet with id: {wallet_id} not found')

    async def save_transaction(
        self, wallet_id: int, amount: Decimal, operation_type: OperationType, description=None,
    ) -> t.NoReturn:
        """

        :param wallet_id:
        :param amount:
        :param operation_type:
        :param description: Addition info about transaction
        :return:
        """
        try:
            await self.connection.fetchval(
                sa.insert(models.transaction).values(
                    wallet_id=wallet_id,
                    amount=amount,
                    type=operation_type,
                    description=description,
                ),
            )
        except asyncpg.exceptions.ForeignKeyViolationError:
            raise errors.NotFound(f'Wallet with id: {wallet_id} not found')
