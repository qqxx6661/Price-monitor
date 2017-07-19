#!/usr/bin/env python
# coding:utf-8
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
import re
import json
import random
import requests
from ua import RandomHeader
from logger import logger
from config import CRAWLER_CONFIG, API_CONFIG
from proxysites import get_proxy_sites

CRAWLER_POOL = Pool(CRAWLER_CONFIG['THREAD_NUM'])
rh = RandomHeader()


class Crawler(object):
    def run(self):
        proxy_sites = self._get_proxy_sites()
        random.shuffle(proxy_sites)
        proxies_list = CRAWLER_POOL.map(self.crawl, proxy_sites)
        proxies = tuple(set([item for sublist in proxies_list for item in sublist]))
        logger.info('Get %s proxies' % len(proxies))
        return proxies

    def crawl(self, site):
        site_url = site[0]
        pattern = site[1]
        proxies = []
        r = None
        try:
            r = requests.get(site_url, headers=rh.Header(site_url), timeout=CRAWLER_CONFIG['TIMEOUT'])
        except:
            pass
        COUNT = 0
        while CRAWLER_CONFIG['RETRY_TIMES'] > COUNT:
            if not r or (not r.ok) or len(r.content) < 500:
                try:
                    port = API_CONFIG['PORT']
                    pr = requests.get('http://localhost:%s/?type=3' % port)
                    proxy = json.loads(pr.content)
                    if proxy:
                        proxy = proxy[0]
                        r = requests.get(site_url, headers=rh.Header(site_url), timeout=CRAWLER_CONFIG['TIMEOUT'],
                                         proxies={'http': 'http://%s' % proxy})
                    else:
                        break
                except Exception, e:
                    pass
                COUNT += 1
            else:
                break
        if not r or not r.ok:
            return []
        for match in pattern.finditer(r.content):
            ip = match.groupdict()['ip']
            port = match.groupdict()['port']
            proxies.append('%s:%s' % (ip, port))
        logger.info('%s crawl ip: %s', site_url, len(proxies))
        return proxies

    def _get_proxy_sites(self):
        proxy_sites = []
        tmp = get_proxy_sites()
        for site in tmp:
            url = site['url']
            pattern = re.compile(site['pattern'])
            if site['range']:
                for i in site['range']:
                    proxy_sites.append((url % i, pattern))
            else:
                proxy_sites.append((url, pattern))
        return proxy_sites


if __name__ == '__main__':
    Crawler().run()
