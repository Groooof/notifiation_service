from fastapi import APIRouter, Depends
from core import schemas
import uuid
from core.storage.database import database
from asyncpg import Connection
import sqlalchemy.ext.asyncio as as_sa
from core.storage import queries

router = APIRouter(prefix='/api/v1', tags=['Main'])

# CLIENT --------------------------------------------------------------------


@router.post('/client')
async def add_client(client_data: schemas.Client, db: as_sa.AsyncConnection = Depends(database.connection)):
    await queries.add_client(db, client_data)
    return {'OK': 'OK'}


@router.put('/client/{id}')
async def update_client(client_data: schemas.UpdateClient, id: uuid.UUID, db: as_sa.AsyncConnection = Depends(database.connection)):
    return client_data.dict()


@router.delete('/client/{id}')
async def delete_client(id: uuid.UUID, db: as_sa.AsyncConnection = Depends(database.connection)):
    return {'id': id}

# STATS ---------------------------------------------------------------------


@router.get('/statistics/total')
async def get_total_stats(db: as_sa.AsyncConnection = Depends(database.connection)):
    res = await queries.get_smth(db)
    return res[0]


@router.get('/statistics/detail')
async def get_detailed_stats(db: as_sa.AsyncConnection = Depends(database.connection)):
    return {'Hello': 'world'}

# MAILING -------------------------------------------------------------------


@router.post('/mailing')
async def add_mailing(mailing_data: schemas.Mailing, db: as_sa.AsyncConnection = Depends(database.connection)):
    return mailing_data.dict()


@router.put('/mailing/{id}')
async def update_mailing(mailing_data: schemas.UpdateMailing, id: uuid.UUID, db: as_sa.AsyncConnection = Depends(database.connection)):
    return mailing_data.dict()


@router.delete('/mailing/{id}')
async def delete_mailing(id: uuid.UUID, db: as_sa.AsyncConnection = Depends(database.connection)):
    return {'id': id}


@router.post('/')
async def hmm():
    return 'HMM'



