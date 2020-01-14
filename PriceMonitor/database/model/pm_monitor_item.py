# coding: utf-8
from sqlalchemy import Column, DateTime, String, create_engine
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class PmMonitorItem(Base):
    __tablename__ = 'pm_monitor_item'

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(INTEGER(11), nullable=False)
    user_price = Column(String(10), nullable=False)
    item_id = Column(BIGINT(20), nullable=False)
    category_id = Column(BIGINT(20))
    name = Column(String(256))
    subtitle = Column(String(512))
    price = Column(String(32))
    plus_price = Column(String(32))
    max_price = Column(String(32))
    min_price = Column(String(32))
    discount = Column(String(32))
    last_price = Column(String(32))
    note = Column(String(128), comment='备注（保留字段）')
    sale = Column(String(128))
    label = Column(String(128))
    store_name = Column(String(128))
    is_ziying = Column(TINYINT(1), comment='是否自营')
    is_alert = Column(TINYINT(1), nullable=False, comment='是否已经提醒')
    gmt_create = Column(DateTime)
    gmt_modified = Column(DateTime)

if __name__ == '__main__':
    engine = create_engine('mysql+pymysql://root:root@localhost/pricemonitor?charset=utf8', echo=True)
    Base.metadata.create_all(engine)