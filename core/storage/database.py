import asyncio
import asyncpg
import typing as tp
from contextlib import asynccontextmanager, contextmanager
import sqlalchemy.ext.asyncio as as_sa
from abc import ABCMeta, abstractmethod
from sqlalchemy.pool import AsyncAdaptedQueuePool
import sqlalchemy as sa
import core.storage.models as md


class IDatabase:
    __metaclass__ = ABCMeta

    @abstractmethod
    async def on_startup(self, host: str, port: str, user: str, password: str, database: str) -> None:
        pass

    @abstractmethod
    async def on_shutdown(self) -> None:
        pass

    @abstractmethod
    async def connection(self):
        pass

    @abstractmethod
    def get_dsn(self, host: str, port: str, user: str, password: str, database: str) -> str:
        pass


class ASPGDatabase(IDatabase):
    def __init__(self):
        self.pool: tp.Optional[asyncpg.Pool] = None

    async def on_startup(self, host, port, user, password, database) -> None:
        self.pool = await asyncpg.create_pool(host=host, port=port, user=user, password=password, database=database)

    async def on_shutdown(self) -> None:
        await self.pool.close()

    async def connection(self) -> asyncpg.Connection:
        if self.pool is None:
            raise NotImplementedError('DB pool must be created first')
        con = await self.pool.acquire()
        try:
            yield con
        finally:
            await self.pool.release(con)

    def get_dsn(self, host: str, port: str, user: str, password: str, database: str) -> str:
        return f'postgres://{user}:{password}@{host}:{port}/{database}'


class ASSADatabase(IDatabase):
    default_driver = 'postgresql'
    default_dialect = 'asyncpg'

    def __init__(self):
        self.engine: tp.Optional[as_sa.AsyncEngine] = None

    async def on_startup(self, host: str, port: str, user: str, password: str, database: str) -> None:
        dsn = self.get_dsn(host, port, user, password, database)
        self.engine = as_sa.create_async_engine(dsn, poolclass=AsyncAdaptedQueuePool, pool_size=5, max_overflow=0)

    async def on_shutdown(self) -> None:
        pass

    async def connection(self) -> as_sa.AsyncConnection:
        if self.engine is None:
            raise NotImplementedError('Engine must be created first')
        con = await self.engine.connect()
        try:
            yield con
            await con.commit()
        except Exception as ex:
            con.rollback()
        finally:
            await con.close()

    @classmethod
    def get_dsn(cls, host, port, user, password, database) -> str:
        return f'{cls.default_driver}+{cls.default_dialect}://{user}:{password}@{host}:{port}/{database}'


database = ASSADatabase()
# database = ASPGDatabase()
#
#
# async def main():
#     await database.on_startup(host='localhost', port=5555, user='albert', password='root', database='notifications')
#     await sa_database.on_startup(host='localhost', port=5555, user='albert', password='root', database='notifications')
#
#     async with asynccontextmanager(database.connection)() as con:
#         res = await con.fetch('SELECT 1 as name')
#         print(type(res[0]))
#
#     async with asynccontextmanager(sa_database.connection)() as con:
#         res = (await con.execute(sa.select(md.mailings)))#.fetchall()
#         print(type(res))
#         print(res.first().filter)
#         print(list(filter(lambda x: not x.startswith('_'), dir(res))))


# asyncio.run(main())
