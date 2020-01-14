# coding: utf-8
from sqlalchemy import Column, DateTime, String, text, create_engine
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class PmUser(Base):
    __tablename__ = 'pm_user'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(40))
    email = Column(String(40), nullable=False, unique=True)
    phone = Column(String(20))
    password = Column(String(255), nullable=False)
    is_active = Column(TINYINT(1), nullable=False, comment='是否活跃账号')
    is_superuser = Column(TINYINT(1), nullable=False, comment='是否管理员')
    is_olduser = Column(TINYINT(1), server_default=text("'0'"))
    gmt_create = Column(DateTime)
    gmt_modified = Column(DateTime)

if __name__ == '__main__':
    engine = create_engine('mysql+pymysql://root:root@localhost/pricemonitor?charset=utf8', echo=True)
    Base.metadata.create_all(engine)