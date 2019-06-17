#!/usr/bin/env python3
# coding=utf-8
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_db import Base, User, Monitor
import datetime
from CONFIG import UPDATE_TIME


class Sql(object):
    engine = create_engine('sqlite:///db_demo.db', echo=True)
    # engine = create_engine('mysql+pymysql://root:root@localhost/pricemonitor?charset=utf8&autocommit=true')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    def write_user(self, user_name, email_address):
        new_user = User(user_name=user_name, email=email_address)
        self.session.add(new_user)
        self.session.commit()

    def write_item(self, item_info):  # item_id, user_price, user_id
        # TODO:修改到这里
        time_now = datetime.datetime.now()
        exist = self.session.query(Monitor).filter_by(item_id=item_info[0]).all()
        if len(exist):  # item already exists in category database
            logging.info('Item id %s already exists in database, update information', item_info[0])
            exist[0].item_name = item_info[1]
            exist[0].subtitle = item_info[3]
            exist[0].update_time = time_now
            if exist[0].item_price != item_info[2]:  # if new price, calculate discount and last_price
                exist[0].status = 1  # set status to 1 for send new alert mail
                exist[0].last_price = exist[0].item_price
                exist[0].item_price = item_info[2]
                logging.debug('last price: {} {}, price: {} {}'.format(type(exist[0].last_price), exist[0].last_price,
                                                                       type(item_info[2]), item_info[2]))
                exist[0].discount = round(float(item_info[2]) / float(exist[0].last_price), 2)
                logging.warning('Item id %s changed price: %s to %s', item_info[0], exist[0].last_price, item_info[2])
        else:
            new_item = Monitor(item_id=item_info[0], user_price=item_info[1], user_id=item_info[2], status=1,
                               add_time=time_now, update_time=time_now)
            self.session.add(new_item)
        self.session.commit()

    def read_all_not_updated_item(self):
        time_now = datetime.datetime.now()
        items_need = []
        items_all = self.session.query(Monitor).all()
        for item_all in items_all:
            item_need = {}
            if item_all.status == 1:
                time_delta = (time_now - item_all.update_time).days * 86400 + (time_now - item_all.update_time).seconds
                logging.info('%s\'s time delta: %s', item_all.item_id, time_delta)
                if time_delta >= UPDATE_TIME:
                    item_need['column_id'] = item_all.column_id
                    item_need['item_id'] = item_all.item_id
                    items_need.append(item_need)
        return items_need

    def update_item_name(self, column_id, item_name):
        update_item = self.session.query(Monitor).get(column_id)
        update_item.item_name = item_name
        self.session.commit()

    def update_item_price(self, column_id, item_price):
        time_now = datetime.datetime.now()
        update_item = self.session.query(Monitor).get(column_id)
        if update_item.item_price and update_item.item_price != item_price:  # if new price
            update_item.last_price = update_item.item_price
            update_item.discount = round(float(item_price) / float(update_item.last_price), 2)  # round(,2) set to 0.01
        update_item.item_price = item_price
        update_item.update_time = time_now
        self.session.commit()

    def update_item_subtitle(self, column_id, subtitle):
        update_item = self.session.query(Monitor).get(column_id)
        update_item.subtitle = subtitle
        self.session.commit()

    def update_item_plus_price(self, column_id, plus_price):
        update_item = self.session.query(Monitor).get(column_id)
        update_item.plus_price = plus_price
        self.session.commit()

    def update_item_max_price(self, column_id, highest_price):
        update_item = self.session.query(Monitor).get(column_id)
        update_item.highest_price = highest_price
        self.session.commit()

    def update_item_min_price(self, column_id, lowest_price):
        update_item = self.session.query(Monitor).get(column_id)
        update_item.lowest_price = lowest_price
        self.session.commit()

    def update_status(self, column_id):
        update_item = self.session.query(Monitor).get(column_id)
        update_item.status = 0
        self.session.commit()

    def check_item_need_to_remind(self):
        # items_alert = {column_id, item_id, user_price, item_price, name, email}
        items_alert = []
        items = self.session.query(Monitor).all()
        for item in items:
            item_alert = {}
            if item.status == 1 and item.user_price:
                if float(item.user_price) > float(item.item_price):
                    user = self.session.query(User).filter_by(column_id=item.user_id)
                    item_alert['email'] = user[0].email
                    item_alert['name'] = item.item_name
                    item_alert['item_price'] = item.item_price
                    item_alert['user_price'] = item.user_price
                    item_alert['item_id'] = item.item_id
                    item_alert['column_id'] = item.column_id
                    items_alert.append(item_alert)
        return items_alert


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    sql = Sql()

    # add user named 'test'
    # sql.write_user('test', 'xxxxxxxxxxx@qq.com')

    # add test item
    sql.write_item(['5544068', '15', '1'])

    # read all items needed update
    # print(sql.read_all_not_updated_item(600))

    # read all user emails for category user
    # print(sql.check_cate_user_mail('Monitor'))

    # update all items needed update
    # sql.update_item_name(1, '123456')

    # check all items needed to send email
    # print(sql.check_cate_item_need_to_remind())
