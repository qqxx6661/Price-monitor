#!/usr/bin/env python3
# coding=utf-8
from gevent import monkey  # IMPORT: must import gevent at first
monkey.patch_all()
from gevent.pool import Pool
from proxy import Proxy
from crawler_selenium import Crawler
from conn_sql import Sql
from mail import Mail
from CONFIG import ITEM_CRAWL_TIME, UPDATE_TIME, Email_TIME, PROXY_CRAWL, THREAD_NUM
import logging
import logging.config
import time
from os import path  # Supervisor cannot find logger.conf
CRAWLER_POOL = Pool(THREAD_NUM)


class Entrance(object):

    proxy_info_zhima= ()

    def _item_info_update(self, items):
        column_id = items[0]
        item_id = items[1]
        item_id = str(item_id)
        sq = Sql()
        pr = Proxy()
        if PROXY_CRAWL == 1:
            # Using free proxy pool
            while True:
                proxy_info = pr.get_proxy()  # tuple: header, proxy
                cr = Crawler(proxy_info[1])
                item_info = cr.get_jd_item(item_id)
                if item_info:  # name, price, subtitle, plus_price
                    sq.update_item_name(column_id, item_info[0])
                    sq.update_item_price(column_id, item_info[1])
                    sq.update_item_subtitle(column_id, item_info[2])
                    sq.update_item_plus_price(column_id, item_info[3])
                    cr = Crawler(proxy_info[1])  # MUST create new instance otherwise got error
                    huihui_info = cr.get_huihui_item(item_id)
                    if huihui_info:  # skip this if not crawled
                        sq.update_item_max_price(column_id, huihui_info[0])
                        sq.update_item_min_price(column_id, huihui_info[1])
                    break
        elif PROXY_CRAWL == 2:
            # Using zhima proxy
            while True:
                if not self.proxy_info_zhima:
                    self.proxy_info_zhima = pr.get_proxy_zhima()
                logging.info('Zhima proxy: %s', self.proxy_info_zhima[1])
                cr = Crawler(self.proxy_info_zhima[1])
                item_info = cr.get_jd_item(item_id)
                if not item_info:
                    self.proxy_info_zhima = ()
                    logging.warning('Zhima proxy crawl failure, changing proxy...')
                    time.sleep(5)
                    continue
                else:
                    sq.update_item_name(column_id, item_info[0])
                    sq.update_item_price(column_id, item_info[1])
                    sq.update_item_subtitle(column_id, item_info[2])
                    sq.update_item_plus_price(column_id, item_info[3])
                    cr = Crawler(self.proxy_info_zhima[1])  # MUST create new instance otherwise got error
                    huihui_info = cr.get_huihui_item(item_id)
                    if huihui_info:  # skip this if not crawled
                        sq.update_item_max_price(column_id, huihui_info[0])
                        sq.update_item_min_price(column_id, huihui_info[1])
                    break
        else:
            # Using local ip
            cr = Crawler()
            item_info = cr.get_jd_item(item_id)
            sq.update_item_name(column_id, item_info[0])
            sq.update_item_price(column_id, item_info[1])
            sq.update_item_subtitle(column_id, item_info[2])
            sq.update_item_plus_price(column_id, item_info[3])
            cr = Crawler()  # MUST create new instance otherwise got error
            huihui_info = cr.get_huihui_item(item_id)
            sq.update_item_max_price(column_id, huihui_info[0])
            sq.update_item_min_price(column_id, huihui_info[1])
        return item_info

    @staticmethod
    def _check_item():
        sq = Sql()
        updated_time = UPDATE_TIME
        items = sq.read_all_not_updated_item(updated_time)
        logging.warning('This loop: %s', items)
        return items

    @staticmethod
    def _send_email():
        # Send email in a loop, avoid sending simultaneously.
        sq = Sql()
        items = sq.check_item_need_to_remind()  # monitor_items, alert_items
        logging.warning('This loop sent email: %s', items)
        for item in items[0]:  # email, item_name, item_price, user_price, item_id, column_id
            item_url = 'https://item.jd.com/' + str(item[4]) + '.html'
            email_text = '您监控的物品：' + item[1] + '，现在价格为：' + item[2] + \
                         '，您设定的价格为：' + item[3] + '，赶紧购买吧！' + item_url
            email_subject = '您监控的物品降价了！'
            try:
                send_email = Mail(email_text, 'admin', 'user', email_subject, item[0])
                send_email.send()
                time.sleep(Email_TIME)
            except:
                logging.critical('Sent email failure, skip in this loop: %s', item[0])
                continue
            sq.update_status(item[5])
            logging.warning('Sent monitor email SUCCESS: %s', item[0])
        for item in items[1]:  # email, item_name, item_price, discount, item_id, column_id, last_price
            item_url = 'https://item.jd.com/' + str(item[4]) + '.html'
            email_text = '您监控的类别中，物品：' + item[1] + '，上次监控价格为：' + item[6] + \
                         '，现在价格为：' + item[2] + '，降价幅度为：' + str(100 * float(item[3])) + '折，赶紧购买吧！' + item_url
            email_subject = '您监控类别中的物品大幅度降价了！'
            try:
                send_email = Mail(email_text, 'admin', 'user', email_subject, item[0])
                send_email.send()
                time.sleep(Email_TIME)
            except:
                logging.critical('Sent email failure, skip in this loop: %s', item[0])
                continue
            sq.update_status(item[5])
            logging.warning('Sent monitor email SUCCESS: %s', item[0])

    def run(self):
        while True:
            update_items = self._check_item()  # tuple: column_id, item_id
            items_info = CRAWLER_POOL.map(self._item_info_update, update_items)  # return two values as a tuple
            logging.warning('This loop updated information: %s', items_info)
            self._send_email()
            time.sleep(ITEM_CRAWL_TIME)


if __name__ == '__main__':
    # Supervisor got permission error, temporarily not using logging
    log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logger.conf')
    logging.config.fileConfig(log_file_path)
    # logger = logging.getLogger("console_file_1")
    logger = logging.getLogger("console_file_2")
    ent = Entrance()
    ent.run()



