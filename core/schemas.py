import pydantic as pd
import datetime as dt
import typing as tp
import re
import uuid
from enum import Enum


local_tz = dt.timezone(dt.timedelta(hours=3), 'Moscow')


class MailingFilter(pd.BaseModel):
    tags: tp.Optional[tp.List[str]]
    codes: tp.Optional[tp.List[str]]

    class Config:
        schema_extra = {
            'example': {
                'tags': ['test_1', 'test_2'],
                'codes': ['978', '912'],
            }
        }


class Mailing(pd.BaseModel):
    id: tp.Optional[uuid.UUID]
    date_start: dt.datetime
    date_stop: dt.datetime
    text: str
    filter: MailingFilter

    class Config:
        schema_extra = {
            'example': {
                'id': '00000000-0000-0000-0000-000000000000',
                'date_start': '2022-01-01T12:00:00.000000+03:00',
                'date_stop': '2022-01-01T15:00:00.000000+03:00',
                'text': 'Some text...',
                'filter': {'tags': ['test_1', 'test_2'],
                           'codes': ['978', '912']},
            }
        }


class UpdateMailing(pd.BaseModel):
    date_start: tp.Optional[dt.datetime]
    date_end: tp.Optional[dt.datetime]
    text: tp.Optional[str]
    filter: tp.Optional[MailingFilter]

    class Config:
        schema_extra = {
            'example': {
                'date_start': '2022-01-01T12:00:00.000000+03:00',
                'date_stop': '2022-01-01T15:00:00.000000+03:00',
                'text': 'Some text...',
                'filter': {'tags': ['test_1', 'test_2'],
                           'codes': ['978', '912']},
            }
        }


def validate_phone(phone):
    regex = '^7[0-9]{10}$'
    if not re.search(regex, phone):
        raise ValueError('Wrong phone format')
    return phone


class Client(pd.BaseModel):
    id: tp.Optional[uuid.UUID]
    phone: str
    code: str
    tag: str
    tz: str

    _phone_validator = pd.validator('phone', allow_reuse=True)(validate_phone)

    class Config:
        schema_extra = {
            'example': {
                'id': '00000000-0000-0000-0000-000000000000',
                'phone': '79781112233',
                'code': '978',
                'tag': 'test',
                'tz': 'Moscow',
            }
        }


class UpdateClient(pd.BaseModel):
    phone: tp.Optional[str]
    code: tp.Optional[str]
    tag: tp.Optional[str]
    tz: tp.Optional[str]

    _phone_validator = pd.validator('phone', allow_reuse=True)(validate_phone)

    class Config:
        schema_extra = {
            'example': {
                'phone': '79781112233',
                'code': '978',
                'tag': 'test',
                'tz': 'Moscow',
            }
        }


class Status(str, Enum):
    success = 'Отправлено'
    in_process = 'Отправляется'
    failed = 'Ошибка'


class Message(pd.BaseModel):
    id: tp.Optional[uuid.UUID]
    created_at: dt.datetime
    status: Status
    mailing_id: uuid.UUID
    client_id: uuid.UUID

    class Config:
        schema_extra = {
            'example': {
                'id': '00000000-0000-0000-0000-000000000000',
                'created_at': '2022-01-01T12:00:00.000000+03:00',
                'status': 'Отправлено',
                'mailing_id': '00000000-0000-0000-0000-000000000000',
                'client_id': '00000000-0000-0000-0000-000000000000',
            }
        }

