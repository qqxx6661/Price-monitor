#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import time
import redis
import logging
import requests
from PriceMonitor.crawler import Crawler
from PriceMonitor.CONFIG import PROXY_POOL_IP
USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0",
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',  # search engine header
    'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)',
    'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
    'DuckDuckBot/1.0; (+http://duckduckgo.com/duckduckbot.html)',
    'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
    'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
    'ia_archiver (+http://www.alexa.com/site/help/webmasters; crawler@alexa.com)'
]


class Proxy(object):

    @staticmethod
    def check_jd_name(proxy, header):
        logging.info('Validating name proxy: %s', proxy)
        item_name = Crawler.get_name_jd('5089253', header, proxy)  # Iphone X
        if '手机' in item_name:
            return True
        return False

    @staticmethod
    def check_jd_price(proxy, header):
        logging.info('Validating price proxy: %s', proxy)
        item_price = Crawler.get_price_jd('5089253', header, proxy)  # Iphone X
        if item_price:
            return True
        return False

    def get_proxy(self, proxy_option):
        r = redis.Redis(host=PROXY_POOL_IP, port=6379, db=0)
        while True:
            good_proxies = r.srandmember("good_proxies", 1)
            if good_proxies:
                good_proxies = good_proxies[0].decode("utf-8")  # byte to str
                good_proxies = {"http": good_proxies, "https": good_proxies}
                header = self.get_ua()
                if proxy_option == 0:  # jd_name
                    if not self.check_jd_name(good_proxies, header):
                        logging.warning('Validate name proxy failure, retrying')
                        continue
                else:  # jd_price
                    if not self.check_jd_price(good_proxies, header):
                        logging.warning('Validate price proxy failure, retrying')
                        continue
                logging.info('Validate SUCCESS，using proxy: %s', good_proxies)
                return header, good_proxies
            else:
                logging.critical('No proxy now from remote server, retrying')
                time.sleep(5)

    def get_proxy_zhima(self):
        url = 'http://webapi.http.zhimacangku.com/getip?num=1&type=2&pro=0' \
              '&city=0&yys=0&port=11&pack=8241&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='
        while True:
            header = self.get_ua()
            r = requests.get(url, headers=header, timeout=5)
            logging.warning('Zhima Proxy: %s', r.json())
            if not r.json()['data']:
                logging.warning('No Zhima Proxy anymore or too fast. Retrying')
                time.sleep(5)
                continue
            try:
                proxy_ip = r.json()['data'][0]['ip']
                proxy_port = r.json()['data'][0]['port']
                good_proxies = proxy_ip + ':' + str(proxy_port)
                good_proxies = {"http": good_proxies, "https": good_proxies}
                return header, good_proxies
            except:
                logging.warning('No Zhima Proxy now. Retrying')
                time.sleep(5)
                continue

    @staticmethod
    def get_ua():
        ua = random.choice(USER_AGENT_LIST)
        ua = {'user-agent': ua}  # dict
        logging.info('Generating header: %s', ua)
        return ua


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    p = Proxy()
    p.get_ua()
    p.get_proxy(1)
