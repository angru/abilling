import contextlib
import typing as t

import asyncpgsa
from asyncpg.pool import Pool

ExecutorType = t.TypeVar('ExecutorType')


class Db:
    pool: Pool = None

    def __init__(self, url, min_size=1, max_size=1):
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

    def connection(self):
        return self.pool.acquire()

    def transaction(self):
        return self.pool.transaction()


@contextlib.asynccontextmanager
async def execute(pool, executor: t.Type[ExecutorType], transaction: bool = False) -> ExecutorType:
    """
    :param pool: pool to acqure connection
    :param executor: who will execute queries
    :param transaction: execute in transaction mode
    :return:
    """
    conn = pool.transaction() if transaction else pool.acquire()

    async with conn as connection:
        yield executor(connection)


class Executor:
    """Не то чтобы я хотел это в прод тащить, просто хотелось поэкперементировать,
    как можно работать с одной транзакцией без:
        * передачи в каждый метод для работы с БД обьекта транзакции/соединения
        * синглтонов клиента БД на инициализируемых на уровне модуля
        * декораторов
    """
    connection = None

    def __init__(self, connection):
        self.connection = connection
