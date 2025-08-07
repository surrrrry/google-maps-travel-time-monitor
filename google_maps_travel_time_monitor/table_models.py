#! /usr/bin/env python

from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.orm import declarative_base
from sqlalchemy import UniqueConstraint
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Index
from sqlalchemy import Text
from sqlalchemy import Float
from sqlalchemy import Date
from peaklib import sqla


def get_snapshot_model(table_name: str):
    unique_column_key = [
        'utc_datetime',
        'route_name',
    ]

    DynamicBase = sqla.get_declarative_base(class_registry=dict())
    class GoogleMapsTravelTimeSnapshotModel(DynamicBase):
        __tablename__ = table_name
        id = Column(Integer, primary_key=True)

        utc_datetime = Column(DateTime, index=True)
        route_name = Column(String(128), index=True)
        start = Column(String(128))
        end = Column(String(128))
        miles = Column(Float)
        minutes = Column(Float)

        created_at = Column(DateTime, index=True)
        last_updated = Column(DateTime)

        __table_args__ = (
            UniqueConstraint(*unique_column_key, name='idx_unique_record'),)

    return GoogleMapsTravelTimeSnapshotModel
