import asyncpg
import typing as tp


class Database:
    def __init__(self):
        self.pool: tp.Optional[asyncpg.Pool] = None

    async def create_pool(self, host, port, user, password, database) -> None:
        self.pool = await asyncpg.create_pool(host=host, port=port, user=user, password=password, database=database)

    async def close_pool(self) -> None:
        await self.pool.close()

    async def connection(self) -> asyncpg.Connection:
        if self.pool is None:
            raise NotImplementedError('DB pool must be created first')
        con = await self.pool.acquire()
        try:
            yield con
        finally:
            await self.pool.release(con)


database = Database()
