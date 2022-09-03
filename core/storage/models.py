import asyncpg
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID as sa_UUID
import uuid
from core.schemas import Status
from sqlalchemy_utils import CompositeType


class Dotdict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class AsyncCompositeType(CompositeType):
    def result_processor(self, dialect, coltype):
        def process(record):
            if isinstance(record, asyncpg.Record):
                return Dotdict(record)
            return record
        return process


meta = sa.MetaData()

CompositeFilter = AsyncCompositeType('mailing_filter', [
    sa.Column('tags', sa.ARRAY(sa.String)),
    sa.Column('codes', sa.ARRAY(sa.String))
])

mailings = sa.Table('mailings', meta,
                    sa.Column('id', sa_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
                    sa.Column('date_start', sa.DateTime, nullable=False),
                    sa.Column('date_stop', sa.DateTime, nullable=False),
                    sa.Column('text', sa.String(1024), nullable=False),
                    sa.Column('filter', CompositeFilter)
                    )

clients = sa.Table('clients', meta,
                   sa.Column('id', sa_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
                   sa.Column('phone', sa.String(11), nullable=False),
                   sa.Column('code', sa.String(3), nullable=False),
                   sa.Column('tag', sa.String(255), nullable=False),
                   sa.Column('tz', sa.String(8), nullable=False)
                   )

messages = sa.Table('messages', meta,
                    sa.Column('id', sa_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
                    sa.Column('created_at', sa.DateTime, nullable=False),
                    sa.Column('status', sa.Enum(Status), nullable=False),
                    sa.Column('mailing_id', sa.Integer, nullable=False),
                    sa.Column('client_id', sa.Integer, nullable=False)
                    )


# @event.listens_for(meta, 'before_create')
# def receive_before_create(target, connection, **kw):
#     print('suka\n'*20)
#     CompositeFilter.create(connection)
#     # before_create(target, connection, **kw)
#
#
# def before_create_2(target, connection, **kw):
#     print('suka\n'*20)
#     CompositeFilter.create(connection)
#
#
# event.listen(meta, 'before_create', before_create_2)

