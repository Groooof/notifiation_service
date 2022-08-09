import pydantic as pd
import datetime as dt
import typing as tp
import re
import uuid


class Mailing(pd.BaseModel):
    id: uuid.UUID
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
    id: uuid.UUID
    phone: int
    code: int
    tag: str
    tz: str

    @pd.validator('phone')
    def phone_validation(cls, v):
        regex = '^7[0-9]{10}$'
        if not re.search(regex, str(v)):
            raise ValueError('Wrong phone format')
        return v


class UpdateClient(pd.BaseModel):
    phone: tp.Optional[int]
    code: tp.Optional[int]
    tag: tp.Optional[str]
    tz: tp.Optional[str]

    @pd.validator('phone')
    def phone_validation(cls, v):
        regex = '^7[0-9]{10}$'
        if not re.search(regex, str(v)):
            raise ValueError('Wrong phone format')
        return v


class Message(pd.BaseModel):
    id: uuid.UUID
    created_at: dt.datetime
    status: int
    mailing_id: uuid.UUID
    client_id: uuid.UUID


class Settings(pd.BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: str

    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'



