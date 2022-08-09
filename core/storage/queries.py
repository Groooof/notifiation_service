import asyncpg


async def get_smth(db: asyncpg.Connection):
    query = '''
    select 666 as col
    '''
    return await db.fetch(query)

