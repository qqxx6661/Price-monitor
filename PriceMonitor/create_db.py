#!/usr/bin/env python3
# coding=utf-8
# import logging
from sqlalchemy import create_engine, Column, ForeignKey
from sqlalchemy import Integer, String, DateTime, Numeric, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    column_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(32), nullable=False, unique=True)
    email = Column(String(64), nullable=False, unique=True)


class Monitor(Base):
    __tablename__ = 'monitor'
    column_id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer, nullable=False)
    item_name = Column(String(64))
    item_price = Column(String(32))  # Please consider storing Decimal numbers as strings or integers on this platform.
    user_price = Column(String(32))  # for lossless storage.
    user_id = Column(Integer, ForeignKey('user.column_id'))
    mall_id = Column(Integer, nullable=False)
    note = Column(String(128))
    update_time = Column(DateTime)
    add_time = Column(DateTime)
    status = Column(Boolean, nullable=False)
    user = relationship(User)


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    engine = create_engine('sqlite:///db_demo1.db', echo=True)
    Base.metadata.create_all(engine)
