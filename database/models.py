from email.policy import default
from enum import unique
from sqlalchemy import (
    Column,
    Float,
    Integer,
    BIGINT,
    String,
    Text,
    ForeignKey,
    Boolean,
    Table,
    UniqueConstraint,
    JSON,
    DateTime,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base, relationship, backref
import uuid


Base = declarative_base()


def NColumn(*args, **kwargs):
    """Column with nullable on False as default"""
    kwargs["nullable"] = kwargs.get("nullable", False)
    return Column(*args, **kwargs)


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    username = NColumn(Text)


class Item(Base):
    __tablename__ = "Item"

    id = Column(Integer, primary_key=True)
    name = NColumn(Text)
    description = Column(Text)
    price = Column(Integer)
    is_hidden = NColumn(Boolean, default=False)
    view_count = NColumn(Integer, default=0)

    updated_by = Column(ForeignKey("User.id"))
    updated_on = NColumn(DateTime, onupdate=func.now(), server_default=func.now())
    created_by = Column(ForeignKey("User.id"))
    created_on = NColumn(DateTime, server_default=func.now())
