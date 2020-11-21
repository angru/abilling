import typing as t

from abilling.db import Storage


async def create_client(name, storage: Storage):
    async with storage.transaction as connection:
        client = await storage.create_client(name=name, connection=connection)
        wallet = await storage.create_wallet(client_id=client['id'], connection=connection)

        client['wallet'] = wallet

        return client