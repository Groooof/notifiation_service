from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from core import schemas
import uuid
from core.storage.database import database
import sqlalchemy.ext.asyncio as as_sa
from core.storage import queries
import typing as tp


class FixedJSONResponse(JSONResponse):
    def render(self, content: tp.Any) -> bytes:
        resp = {'content': content,
                'code': self.status_code,
                '4len': 'konya'}
        return super().render(resp)


router = APIRouter(prefix='/api/v1', tags=['Main'])

# CLIENT --------------------------------------------------------------------


def get_db_connection(con: as_sa.AsyncConnection = Depends(database.connection)):
    return con


@router.post('/lol')
async def lol(con: as_sa.AsyncConnection = Depends(get_db_connection)):
    res = await queries.get_clients_by_filter(con, tags=['test_1', 'test_2'], codes=['978', '912'])
    return res


@router.post('/client')
async def add_client(client_data: schemas.Client, con: as_sa.AsyncConnection = Depends(get_db_connection)):
    res = await queries.add_client(con, client_data)
    return res


@router.put('/client/{id}')
async def update_client(client_data: schemas.UpdateClient, id: uuid.UUID, con: as_sa.AsyncConnection = Depends(get_db_connection)):
    res = await queries.update_client(con, id, client_data)
    return res


@router.delete('/client/{id}')
async def delete_client(id: uuid.UUID, con: as_sa.AsyncConnection = Depends(get_db_connection)):
    res = await queries.del_client(con, id)
    return res

# STATS ---------------------------------------------------------------------


@router.get('/statistics/total')
async def get_total_stats(con: as_sa.AsyncConnection = Depends(get_db_connection)):
    # res = await queries.get_smth(db)
    # return res[0]
    pass


@router.get('/statistics/detail')
async def get_detailed_stats(con: as_sa.AsyncConnection = Depends(get_db_connection)):
    return {'Hello': 'world'}

# MAILING -------------------------------------------------------------------


@router.post('/mailing')
async def add_mailing(mailing_data: schemas.Mailing, con: as_sa.AsyncConnection = Depends(get_db_connection)):
    res = await queries.add_mailing(con, mailing_data)
    return res


@router.put('/mailing/{id}')
async def update_mailing(mailing_data: schemas.UpdateMailing, id: uuid.UUID, con: as_sa.AsyncConnection = Depends(get_db_connection)):
    res = await queries.update_mailing(con, id, mailing_data)
    return res


@router.delete('/mailing/{id}')
async def delete_mailing(id: uuid.UUID, con: as_sa.AsyncConnection = Depends(get_db_connection)):
    res = await queries.del_mailing(con, id)
    return res


@router.post('/')
async def hmm():
    return 'HMM'



