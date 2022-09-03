import asyncpg
import core.schemas as sch
import core.storage.models as md
import sqlalchemy as sa
from sqlalchemy import select, insert
from sqlalchemy.dialects import postgresql
import sqlalchemy.ext.asyncio as as_sa
import uuid
import datetime as dt
import typing as tp


async def lol(con: as_sa.AsyncConnection):
    data = sch.Mailing(date_start=dt.datetime.now(), date_stop=dt.datetime.now(), text='zaebaaaaal', filter=sch.MailingFilter(tags=['test'], codes=['978']))
    query = md.mailings.insert().values(**data.dict(exclude_none=True)).returning(md.mailings)
    res = (await con.execute(query)).cursor.fetchall()
    print(res)
    for i in res:
        print(type(i), i)
    await con.commit()
    return None


async def add_client(con: as_sa.AsyncConnection, data: sch.Client):
    query = md.clients.insert().values(**data.dict(exclude_none=True)).returning(md.clients)
    res = (await con.execute(query)).fetchall()
    return res


async def update_client(con: as_sa.AsyncConnection, id: uuid.UUID, data: sch.UpdateClient):
    query = md.clients.update().where(md.clients.c.id == id).values(**data.dict(exclude_none=True)).returning(md.clients)
    res = (await con.execute(query)).fetchall()
    return res


async def del_client(con: as_sa.AsyncConnection, id: uuid.UUID):
    query = md.clients.delete().where(md.clients.c.id == id).returning(md.clients.c.id)
    res = (await con.execute(query)).fetchone()
    return res


async def add_mailing(con: as_sa.AsyncConnection, data: sch.Mailing):
    query = md.mailings.insert().values(**data.dict(exclude_none=True)).returning(md.mailings)
    res = (await con.execute(query)).fetchall()
    return res


async def update_mailing(con: as_sa.AsyncConnection, id: uuid.UUID, data: sch.UpdateClient):
    query = md.mailings.update().where(md.mailings.c.id == id).values(**data.dict(exclude_none=True)).returning(md.mailings)
    res = (await con.execute(query)).fetchall()
    return res


async def del_mailing(con: as_sa.AsyncConnection, id: uuid.UUID):
    query = md.mailings.delete().where(md.mailings.c.id == id).returning(md.mailings.c.id)
    res = (await con.execute(query)).fetchone()
    return res


async def get_clients_by_filter(con: as_sa.AsyncConnection, codes: tp.List[str], tags: tp.List[str]) -> tp.List[str]:
    query = sa.select(md.clients.c.phone).where(sa.or_(md.clients.c.tag.in_(tags), md.clients.c.code.in_(codes)))
    cursor = (await con.execute(query))
    return [item.phone for item in cursor]
