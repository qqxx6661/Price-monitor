#!/usr/bin/env python3
# coding=utf-8
from gevent import monkey  # IMPORT: must import gevent at first
monkey.patch_all()
from gevent.pool import Pool
from PriceMonitor.proxy import Proxy
from PriceMonitor.crawler import Crawler
from PriceMonitor.conn_sql import Sql
from PriceMonitor.mail import Mail
from PriceMonitor.CONFIG import CRAWL_TIME, UPDATE_TIME, Email_TIME, PROXY_CRAWL, THREAD_NUM
import logging
import logging.config
import time

CRAWLER_POOL = Pool(THREAD_NUM)


class Entrance(object):

    proxy_info_zhima_name = ()
    proxy_info_zhima_price = ()

    def _item_info_update(self, items):
        column_id = items[0]
        item_id = items[1]
        item_id = str(item_id)
        sq = Sql()
        pr = Proxy()
        if PROXY_CRAWL == 1:
            # Using free proxy pool
            while True:
                proxy_info = pr.get_proxy(0)  # tuple: header, proxy
                name = Crawler.get_name_jd(item_id, proxy_info[0], proxy_info[1])
                if name:
                    sq.update_item_name(column_id, name)
                    while True:
                        proxy_price = pr.get_proxy(1)  # tuple: header, proxy
                        price = Crawler.get_price_jd(item_id, proxy_price[0], proxy_price[1])
                        if price:
                            sq.update_item_price(column_id, price)
                            break
                    break
        elif PROXY_CRAWL == 2:
            # Using zhima proxy
            while True:
                if not self.proxy_info_zhima_name:
                    self.proxy_info_zhima_name = pr.get_proxy_zhima()
                    print('Name proxy:', self.proxy_info_zhima_name, items)
                name = Crawler.get_name_jd(item_id, self.proxy_info_zhima_name[0], self.proxy_info_zhima_name[1])
                if not name:
                    self.proxy_info_zhima_name = ()
                    time.sleep(20)
                    continue
                else:
                    time.sleep(5)  # Avoid get proxy too fast
                    sq.update_item_name(column_id, name)
                    while True:
                        if not self.proxy_info_zhima_price:
                            self.proxy_info_zhima_price = pr.get_proxy_zhima()
                            print('Price proxy:', self.proxy_info_zhima_price, items)
                        price = Crawler.get_price_jd(item_id, self.proxy_info_zhima_price[0], self.proxy_info_zhima_price[1])
                        if not price:
                            self.proxy_info_zhima_price = ()
                            time.sleep(20)
                            continue
                        else:
                            sq.update_item_price(column_id, price)
                            break
                    break
        else:
            # Using local ip
            name = Crawler.get_name_jd(item_id, pr.get_ua())
            sq.update_item_name(column_id, name)
            price = Crawler.get_price_jd(item_id, pr.get_ua())
            sq.update_item_price(column_id, price)
            return name, price

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
        items = sq.check_item_need_to_remind()
        logging.warning('This loop sent email: %s', items)
        for item in items:  # email, item_name, item_price, user_price, item_id, column_id
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
            logging.warning('Sent email SUCCESS: %s', item[0])

    def run(self):
        while True:
            items = self._check_item()  # tuple: column_id, item_id
            items_info = CRAWLER_POOL.map(self._item_info_update, items)  # return two values as a tuple
            logging.warning('This loop updated information: %s', items_info)
            self._send_email()
            time.sleep(CRAWL_TIME)


if __name__ == '__main__':

    logging.config.fileConfig("logger.conf")
    logger = logging.getLogger("console_file_2")
    ent = Entrance()
    ent.run()



