import asyncpgsa
from asyncpg.pool import Pool

from abilling import models


class Storage:
    pool: Pool = None

    def __init__(self, url):
        self.url = url

    async def init(self):
        self.pool = await asyncpgsa.create_pool(
            dsn=self.url,
            min_size=3,
            max_size=10,
        )

    @property
    def connection(self):
        return self.pool.acquire()

    @property
    def transaction(self):
        return self.pool.transaction()

    async def create_client(self, name, connection):
        result = await connection.fetchrow(
            models.client.insert(return_defaults=True).values({'name': name}),
        )

        return {
            'id': result['id'],
            'name': name,
            'date': result['date'],
        }

    async def create_wallet(self, client_id, connection):
        result = await connection.fetchrow(
            models.wallet.insert(return_defaults=True).values(client_id=client_id),
        )

        return {
            'id': result['id'],
            'client_id': client_id,
            'balance': result['balance'],
        }


class Client:
    @classmethod
    async def create(cls, name, connection) -> 'Client':
         await connection.fetchrow(
            models.client.insert(return_defaults=True).values({'name': name}),
        )

    @classmethod
    async def get(cls, client_id) -> 'Client':
        pass

    @property
    def id(self) -> int:
        pass

    @property
    def name(self) -> str:
        pass