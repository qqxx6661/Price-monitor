#!/usr/bin/env python3
# coding=utf-8
# import logging
from gevent import monkey  # IMPORT: must import gevent at first
monkey.patch_all()
from sqlalchemy import create_engine, Column, ForeignKey
from sqlalchemy import Integer, String, DateTime, Numeric, Boolean, BIGINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    column_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(32), nullable=False, unique=True)
    email = Column(String(64), nullable=False, unique=True)
    category = Column(String(128))


class Monitor(Base):
    __tablename__ = 'monitor'
    column_id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(BIGINT, nullable=False)
    item_name = Column(String(128))
    item_price = Column(String(32))  # Please consider storing Decimal numbers as strings or integers on this platform.
    user_price = Column(String(32))  # for lossless storage.
    discount = Column(String(32))
    lowest_price = Column(String(32))
    highest_price = Column(String(32))
    last_price = Column(String(32))
    plus_price = Column(String(32))
    subtitle = Column(String(128))
    user_id = Column(Integer, ForeignKey('user.column_id'))
    note = Column(String(128))
    update_time = Column(DateTime)
    add_time = Column(DateTime)
    status = Column(Boolean, nullable=False)
    user = relationship(User)


class SmartPhone_9987653655(Base):
    __tablename__ = 'SmartPhone_9987653655'
    column_id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(BIGINT, nullable=False)
    item_name = Column(String(128))
    item_price = Column(String(32))
    discount = Column(String(32))
    lowest_price = Column(String(32))
    highest_price = Column(String(32))
    last_price = Column(String(32))
    plus_price = Column(String(32))
    subtitle = Column(String(128))
    note = Column(String(128))
    update_time = Column(DateTime)
    add_time = Column(DateTime)
    status = Column(Boolean, nullable=False)

if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    engine = create_engine('sqlite:///db_demo.db', echo=True)
    # engine = create_engine('mysql+pymysql://root:root@localhost/pricemonitor?charset=utf8', echo=True, )
    Base.metadata.create_all(engine)
