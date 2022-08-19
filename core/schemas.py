import pydantic as pd
import datetime as dt
import typing as tp
import re
import uuid
from enum import Enum


class Mailing(pd.BaseModel):
    id: tp.Optional[uuid.UUID] = None
    date_start: dt.datetime
    date_end: dt.datetime
    text: str
    filter: str


class UpdateMailing(pd.BaseModel):
    date_start: tp.Optional[dt.datetime]
    date_end: tp.Optional[dt.datetime]
    text: tp.Optional[str]
    filter: tp.Optional[str]


class Client(pd.BaseModel):
    id: tp.Optional[uuid.UUID] = None
    phone: str
    code: str
    tag: str
    tz: str

    @pd.validator('phone', allow_reuse=True)
    def phone_validation(cls, v):
        regex = '^7[0-9]{10}$'
        if not re.search(regex, str(v)):
            raise ValueError('Wrong phone format')
        return v


class UpdateClient(pd.BaseModel):
    phone: tp.Optional[str]
    code: tp.Optional[str]
    tag: tp.Optional[str]
    tz: tp.Optional[str]

    @pd.validator('phone', allow_reuse=True)
    def phone_validation(cls, v):
        regex = '^7[0-9]{10}$'
        if not re.search(regex, str(v)):
            raise ValueError('Wrong phone format')
        return v


class Status(str, Enum):
    success = 'Отправлено'
    in_process = 'Отправляется'
    failed = 'Ошибка'


class Message(pd.BaseModel):
    id: tp.Optional[uuid.UUID] = None
    created_at: dt.datetime
    status: Status
    mailing_id: uuid.UUID
    client_id: uuid.UUID



