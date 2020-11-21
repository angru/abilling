import contextlib
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
        return execute(self.pool, executor, transaction)


@contextlib.asynccontextmanager
async def execute(pool, executor: t.Type[ExecutorType], transaction=False) -> ExecutorType:
    conn = pool.transaction() if transaction else pool.acquire()

    async with conn as connection:
        yield executor(connection)


class Executor:
    connection = None

    def __init__(self, connection):
        self.connection = connection
