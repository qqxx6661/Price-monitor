#!/usr/bin/env python3
# coding=utf-8
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from PriceMonitor.create_db import Base, User, Monitor
import datetime


class Sql(object):

    engine = create_engine('sqlite:///db_demo.db', echo=True)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    def read_all_item(self):
        all_item = self.session.query(Monitor).all()
        return all_item

    def read_all_not_updated_item(self, update_time):
        time_now = datetime.datetime.now()
        need_item = []
        all_items = self.session.query(Monitor).all()
        for item in all_items:
            if item.status:
                time_delta = (time_now - item.update_time).days * 86400 + (time_now - item.update_time).seconds
                logging.info('%s\'s time delta: %s', item.item_id, time_delta)
                if time_delta >= update_time:
                    need_item.append((item.column_id, item.item_id))
        return need_item

    def check_item_need_to_remind(self):
        need_item = []
        items = self.session.query(Monitor).filter_by(status=1)
        for item in items:
            if float(item.user_price) > float(item.item_price):
                user = self.session.query(User).filter_by(column_id=item.user_id)
                need_item.append([user[0].email, item.item_name, item.item_price,
                                  item.user_price, item.item_id, item.column_id])
        return need_item

    def write_item(self, item_id, user_price, user_id, mall_id=1, status=1):
        time_now = datetime.datetime.now()
        new_item = Monitor(item_id=item_id, user_price=user_price, user_id=user_id,
                           mall_id=mall_id, status=status, add_time=time_now, update_time=time_now)
        self.session.add(new_item)
        self.session.commit()

    def write_user(self, user_name, email_address):
        new_user = User(user_name=user_name, email=email_address)
        self.session.add(new_user)
        self.session.commit()

    def update_item_name(self, column_id, item_name):
        update_item = self.session.query(Monitor).get(column_id)  # get maybe get by id
        update_item.item_name = item_name
        self.session.commit()

    def update_item_price(self, column_id, item_price):
        time_now = datetime.datetime.now()
        update_item = self.session.query(Monitor).get(column_id)  # get maybe get by id
        update_item.item_price = item_price
        update_item.update_time = time_now
        self.session.commit()

    def update_status(self, column_id):
        update_item = self.session.query(Monitor).get(column_id)
        update_item.status = 0
        self.session.commit()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    sql = Sql()

    # add user named 'test'
    # sql.write_user('test', '404013419@qq.com')

    # add test item
    # sql.write_item(2777811, '10', 1)

    # read all items in Monitor
    # items = sql.read_all_item()
    # for item in items:
    #     print(item.item_id)

    # read all items needed update
    # print(sql.read_all_not_updated_item(600))

    # update all items needed update
    # sql.update_item_name(1, '123456')

    # check all items needed to send email
    sql.check_item_need_to_remind()
