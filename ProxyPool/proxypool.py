#!/usr/bin/env python
# coding:utf-8
from gevent import monkey
monkey.patch_all()
import datetime
import time
import threading
from logger import logger
from DB import DatabaseObject
from config import DB_CONFIG, PROXYPOOL_CONFIG, API_CONFIG
from crawler import Crawler
from validator import Validator
from api import ProxyServer


class ProxyPool:
    def __init__(self):
        self.sqlite = DatabaseObject(DB_CONFIG['SQLITE'])
        self.Validator = Validator()
        self.Crawler = Crawler()

    def _monitor(self):
        while True:
            self._update(PROXYPOOL_CONFIG['UPDATE_TIME'])
            self._delete(PROXYPOOL_CONFIG['DELETE_TIME'], PROXYPOOL_CONFIG['DELETE_SCORE'])
            self._crawl(PROXYPOOL_CONFIG['CRAWL_TIME'])
            time.sleep(PROXYPOOL_CONFIG['SLEEP_TIME'])

    def _crawl(self, minutes):
        query = "SELECT COUNT(*) FROM proxy WHERE updatetime>'%s'" % \
                ((datetime.datetime.now() - datetime.timedelta(minutes=minutes)).strftime('%Y-%m-%d %H:%M:%S'))
        count = self.sqlite.executesql(query)[0]
        if int(count[0]) < PROXYPOOL_CONFIG['MIN_IP_NUM']:
            logger.info('Crawl proxy begin')
            proxies = self.Crawler.run()
            logger.info('Crawl proxy end')
            logger.info('Validate proxy begin')
            proxies = [(n, '') for n in proxies]
            avaliable_proxies = self.Validator.run(proxies)
            logger.info('Validate proxy end')
            if DB_CONFIG['SQLITE']:
                self.save2sqlite(avaliable_proxies)
            time.sleep(600)
            self._crawl(minutes)
        else:
            return

    def _delete(self, minutes, score):
        query = "DELETE FROM proxy WHERE updatetime<'%s' or score<%s" % (
        (datetime.datetime.now() - datetime.timedelta(minutes=minutes)).strftime('%Y-%m-%d %H:%M:%S'), score)
        self.sqlite.executesql(query)

    def _update(self, minutes):
        query = "SELECT ip,port,protocol FROM proxy WHERE updatetime<'%s'" % (
        (datetime.datetime.now() - datetime.timedelta(minutes=minutes)).strftime('%Y-%m-%d %H:%M:%S'))
        proxies = [('%s:%s' % n[:2], n[2]) for n in self.sqlite.executesql(query)]
        if proxies:
            avaliable_proxies = self.Validator.run(proxies)
            validated_fail_proxies = list(set([tuple(n[0].split(':')) for n in proxies]).difference(set([(n['ip'], n['port']) for n in avaliable_proxies])))
            self.save2sqlite(avaliable_proxies)
            self._minus_score(validated_fail_proxies)

    def save2sqlite(self, result):
        failed = self.sqlite.insert('proxy', result)
        if failed:
            failed = self.sqlite.update('proxy', failed)
        if failed:
            logger.info('Some ip failed to save: %s' % (str(failed)))

    def _minus_score(self, result):
        query = "UPDATE proxy SET score=(score-1) WHERE ip=? AND port=?;"
        self.sqlite.cursor.executemany(query, result)
        self.sqlite.db.commit()

    def _api(self):
        ProxyServer(API_CONFIG['PORT'])

    def run(self):
        t1 = threading.Thread(target=self._api)
        t2 = threading.Thread(target=self._monitor)
        t1.start()
        t2.start()


if __name__ == '__main__':
    ProxyPool().run()
