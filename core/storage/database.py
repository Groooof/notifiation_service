import asyncio
import asyncpg
import typing as tp
from contextlib import asynccontextmanager, contextmanager
import sqlalchemy.ext.asyncio as as_sa
from abc import ABCMeta, abstractmethod
from sqlalchemy.pool import AsyncAdaptedQueuePool


class IDatabase:
    __metaclass__ = ABCMeta

    @abstractmethod
    def on_startup(self, host: str, port: str, user: str, password: str, database: str) -> None:
        pass

    @abstractmethod
    def on_shutdown(self) -> None:
        pass

    @abstractmethod
    def connection(self):
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

    def on_startup(self, host: str, port: str, user: str, password: str, database: str) -> None:
        dsn = self.get_dsn(host, port, user, password, database)
        self.engine = as_sa.create_async_engine(dsn, poolclass=AsyncAdaptedQueuePool, pool_size=5, max_overflow=0)

    def on_shutdown(self) -> None:
        pass

    def connection(self) -> as_sa.AsyncConnection:
        if self.engine is None:
            raise NotImplementedError('Engine must be created first')
        con = await self.engine.connect()
        try:
            yield con
        finally:
            await con.close()

    @classmethod
    def get_dsn(cls, host, port, user, password, database) -> str:
        return f'{cls.default_driver}+{cls.default_dialect}://{user}:{password}@{host}:{port}/{database}'


database = ASSADatabase()


from core.settings import settings as cfg


import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import event
from timeit import default_timer

# engine = sa.create_engine('sqlite:///:memory:')
# engine = as_sa.create_async_engine(cfg.POSTGRES_DSN, poolclass=AsyncAdaptedQueuePool, pool_size=5, max_overflow=0)
# meta = sa.MetaData()


# queries = [
#     sa.select(i+1) for i in range(700)
# ]


# @event.listens_for(engine.sync_engine, "connect")
# def my_on_connect(dbapi_con, connection_record):
#     print("New DBAPI connection:", dbapi_con)


# async def exec(query):
#     async with engine.connect() as con:
#         res = await con.execute(query)
#         return res.fetchone()[0]
#
#
# async def main():
#     # database = Database()
#     # await database.create_pool(host=cfg.POSTGRES_HOST,
#     #                            user=cfg.POSTGRES_USER,
#     #                            password=cfg.POSTGRES_PASSWORD,
#     #                            database=cfg.POSTGRES_DB,
#     #                            port=cfg.POSTGRES_PORT,
#     #                            min_size=50,
#     #                            max_size=50
#     #                            )
#     tasks = [exec(q) for q in queries]
#     # tasks = [database.pool.fetch(f'SELECT {i+1}') for i in range(2100)]
#     start = default_timer()
#     res = await asyncio.gather(*tasks)
#     [print(r, ',', end='') for r in res]
#     end = default_timer()
#     print(f'\nTime: {end-start}')
#
#     # async with engine.begin() as con:
#     #     tasks = [con.execute(q) for q in queries]
#     #     res = await asyncio.gather(*tasks)
#     #     # res = await con.execute(sa.select(1))
#     #     [print(r.fetchone()) for r in res]
#
# asyncio.run(main())
#
#
# users = sa.Table('users', meta,
#     sa.Column('id', sa.Integer, nullable=False, primary_key=True, default=int),
#     sa.Column('name', sa.String, nullable=False),
#     sa.Column('phone', sa.String, nullable=False)
# )
#
# #meta.create_all(engine)
#
# q1 = users.insert().values(id=1, name='Ffs', phone='123')
# q2 = sa.select(users).where(users.c.id.in_((1, 2, 3)))
#
# # with engine.connect() as con:
# #     with con.begin():
# #         r1 = con.execute(q1)
# #         r2 = con.execute(q2)
# #
# # # for r in r1:
# # #     print(r)
# # for r in r2:
# #     print(r)


