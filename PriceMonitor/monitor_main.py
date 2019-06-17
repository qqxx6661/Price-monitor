#!/usr/bin/env python3
# coding=utf-8
from proxy import Proxy
from crawler_selenium import Crawler
from conn_sql import Sql
from mail import Mail
from CONFIG import ITEM_CRAWL_TIME, Email_TIME, PROXY_CRAWL
import logging
import logging.config
import time
from os import path


class Entrance(object):
    proxy_info_zhima = ()

    @staticmethod
    def _check_item():
        """
        检查本轮需要爬取的商品
        :return: [{column_id, item_id}, ...]
        """
        sq = Sql()
        items = sq.read_all_not_updated_item()
        logging.warning('This loop ready to crawl: %s', items)
        return items

    def _item_info_update(self, item):
        column_id = item['column_id']
        item_id = str(item['item_id'])
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
            # item_info: {name, price, plus_price, subtitle}
            item_info = cr.get_jd_item(item_id)
            sq.update_item_name(column_id, item_info['name'])
            sq.update_item_price(column_id, item_info['price'])
            sq.update_item_plus_price(column_id, item_info['plus_price'])
            sq.update_item_subtitle(column_id, item_info['subtitle'])

            cr = Crawler()
            # huihui_info = {max_price, min_price}
            huihui_info = cr.get_huihui_item(item_id)
            sq.update_item_max_price(column_id, huihui_info['max_price'])
            sq.update_item_min_price(column_id, huihui_info['min_price'])

        return item_info

    @staticmethod
    def _send_email():
        sq = Sql()
        # items_alert = {column_id, item_id, user_price, item_price, name, email}
        items_alert = sq.check_item_need_to_remind()
        logging.warning('This loop sent email: %s', items_alert)
        for item_alert in items_alert:  # item: [email, item_name, item_price, user_price, item_id, column_id]
            item_url = 'https://item.jd.com/' + str(item_alert['item_id']) + '.html'
            email_text = '您监控的物品：' + item_alert['name'] + '，现在价格为：' + item_alert['item_price'] + \
                         '，您设定的价格为：' + item_alert['user_price'] + '，赶紧购买吧！' + item_url
            email_subject = '您监控的物品降价了！'
            try:
                send_email = Mail(email_text, '价格监控系统', '亲爱的用户', email_subject, item_alert['email'])
                send_email.send()
                time.sleep(Email_TIME)
            except:
                logging.critical('Sent email failure, skip in this loop: %s', item_alert['email'])
                continue
            sq.update_status(item_alert['column_id'])
            logging.warning('Sent monitor email SUCCESS: %s', item_alert['email'])

    def run(self):
        while True:
            items = self._check_item()
            for item in items:
                item_info = self._item_info_update(item)
                logging.warning('Update item: %s', item_info)
            self._send_email()
            logging.warning('Ready to sleep: %s', ITEM_CRAWL_TIME)
            time.sleep(ITEM_CRAWL_TIME)


if __name__ == '__main__':
    log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logger.conf')
    logging.config.fileConfig(log_file_path)
    # logger = logging.getLogger("console_file_1")
    logger = logging.getLogger("console_file_2")
    ent = Entrance()
    ent.run()
