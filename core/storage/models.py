from sqlalchemy import Integer, String, Column, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from core.schemas import Status

Base = declarative_base()


class Mailings(Base):
    __tablename__ = 'mailings'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date_start = Column(DateTime, nullable=False)
    date_stop = Column(DateTime, nullable=False)
    text = Column(String(1024), nullable=False)
    filter = Column(String(255), nullable=False)


class Clients(Base):
    __tablename__ = 'clients'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone = Column(String(11), nullable=False)
    code = Column(String(3), nullable=False)
    tag = Column(String(255), nullable=False)
    tz = Column(String(8), nullable=False)


class Messages(Base):
    __tablename__ = 'messages'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, nullable=False)
    status = Column(Enum(Status), nullable=False)
    mailing_id = Column(Integer, nullable=False)
    client_id = Column(Integer, nullable=False)


