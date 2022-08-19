import asyncpg
import core.schemas as sch
import core.storage.models as models
from sqlalchemy import select, insert
from sqlalchemy.dialects import postgresql
import sqlalchemy.ext.asyncio as as_sa


async def add_client(db: as_sa.AsyncConnection, client: sch.Client):
    query = insert(models.Clients).values(**client.dict()).compile(dialect=postgresql.asyncpg.dialect())
    await db.execute(query)

