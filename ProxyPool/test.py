#!/usr/bin/env python
# coding:utf-8
import requests
import json
from config import API_CONFIG, HEADER


url = 'http://www.guokr.com'


def run():
    while True:
        port = API_CONFIG['PORT']
        r = requests.get('http://localhost:%s/' % port)
        proxy = json.loads(r.content)
        if proxy:
            proxy = proxy[0]
        else:
            break
        try:
            r = requests.get(url, headers=HEADER, proxies={'http': 'http://%s' % proxy})
            print r.ok, len(r.content), proxy
        except Exception, e:
            print proxy, e

if __name__ == '__main__':
    run()
