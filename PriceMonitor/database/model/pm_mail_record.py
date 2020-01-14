# coding: utf-8
from sqlalchemy import Column, DateTime, String, text, create_engine
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class PmMailRecord(Base):
    __tablename__ = 'pm_mail_record'

    id = Column(INTEGER(20), primary_key=True, comment='主键id')
    address = Column(String(64), nullable=False, comment='邮箱地址')
    _from = Column('from', String(64), nullable=False, comment='发件人昵称')
    to = Column(String(64), nullable=False, comment='收件人昵称')
    subject = Column(String(64), nullable=False, comment='主题')
    content = Column(String(4096), nullable=False, comment='内容')
    is_sent = Column(TINYINT(3), nullable=False, comment='1-发送成功, 0-发送失败')
    gmt_create = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    gmt_modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')

if __name__ == '__main__':
    engine = create_engine('mysql+pymysql://root:root@localhost/pricemonitor?charset=utf8', echo=True)
    Base.metadata.create_all(engine)
