import typing as t

import asyncpgsa
from asyncpg.pool import Pool


ExecutorType = t.TypeVar('ExecutorType')


class Db:
    pool: Pool = None

    def __init__(self, url, min_size=3, max_size=10):
        self.url = url
        self.min_size = min_size
        self.max_size = max_size

    async def init(self):
        if self.pool is None:
            self.pool = await asyncpgsa.create_pool(
                dsn=self.url,
                min_size=self.min_size,
                max_size=self.max_size,
            )

    async def stop(self):
        if self.pool:
            await self.pool.close()

    def executor(self, executor: t.Type[ExecutorType], transaction=False) -> ExecutorType:
        return executor(
            self.pool,
            in_transaction=transaction,
        )


class Executor:
    connection = None

    def __init__(self, pool, in_transaction=False):
        self.pool = pool
        self.in_transaction = in_transaction

    async def __aenter__(self):
        self.connection = await self.pool._acquire(timeout=None)

        if self.in_transaction:
            self.transaction = self.connection.transaction()

            await self.transaction.start()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.in_transaction:
            if exc_type:
                await self.transaction.rollback()
            else:
                await self.transaction.commit()

        await self.pool.release(self.connection)
