#!/usr/bin/env python
# coding:utf-8


def get_proxy_sites():
    proxysites = [
        {
            'url': 'http://www.66ip.cn/%s.html',
            'range': ['index'] + range(2, 11),
            'pattern': '(?P<ip>(?:\d{1,3}\.){3}\d{1,3})</td>\n?\s*<td.*?>\s*(?P<port>\d{1,4})'
        },
        {
            'url': 'http://www.66ip.cn/%s',
            'range': ['mo.php?tqsl=1000']
                     +
                     ['nmtq.php?getnum=1000&anonymoustype=%s&proxytype=2&api=66ip' % n for n in range(1, 5)],
            'pattern': '(?P<ip>(?:\d{1,3}\.){1,3}\d{1,3}):(?P<port>\d{1,4})'
        },
        {
            'url': 'http://www.66ip.cn/mo.php?sxb=&tqsl=3000&port=&export=&ktip=&sxa=&textarea=',
            'range': [],
            'pattern': '(?P<ip>(?:\d{1,3}\.){1,3}\d{1,3}):(?P<port>\d{1,4})'
        },
        # {
        #     'url': 'http://www.kuaidaili.com/proxylist/%s',
        #     'range': range(1, 11),
        #     'pattern': '(?P<ip>(?:\d{1,3}\.){3}\d{1,3})</td>\n?\s*<td.*?>\s*(?P<port>\d{1,4})'
        # },
        # {
        #     'url': 'http://www.kuaidaili.com/free/%s',
        #     'range': ['%s/%s' % (m, n) for m in ['inha', 'intr', 'outha', 'outtr'] for n in range(1, 11)],
        #     'pattern': '(?P<ip>(?:\d{1,3}\.){3}\d{1,3})</td>\n?\s*<td.*?>\s*(?P<port>\d{1,4})'
        # },
        {
            'url': 'http://www.xicidaili.com/%s',
            'range': ['%s/%s' % (m, n) for m in ['nn', 'nt', 'wn', 'wt'] for n in range(1, 6)],
            'pattern': '(?P<ip>(?:\d{1,3}\.){3}\d{1,3})</td>\n?\s*<td.*?>\s*(?P<port>\d{1,4})'
        },
        {
            'url': 'http://www.cz88.net/proxy/%s',
            'range': ['index.shtml'] + ['http_%s.shtml' % n for n in range(2, 11)],
            'pattern': '(?P<ip>(?:\d{1,3}\.){3}\d{1,3})</div>\n?\s*<div.*?>\s*(?P<port>\d{1,4})'
        },
        {
            'url': 'http://www.ip181.com/daili/%s.html',
            'range': range(1, 11),
            'pattern': '(?P<ip>(?:\d{1,3}\.){3}\d{1,3})</td>\n?\s*<td.*?>\s*(?P<port>\d{1,4})'

        },
        {
            'url': 'http://proxy.ipcn.org/proxylist%s.html',
            'range': ['', '2'],
            'pattern': '(?P<ip>(?:\d{1,3}\.){1,3}\d{1,3}):(?P<port>\d{1,4})'
        },
        {
            'url': 'http://ip84.com/%s',
            'range': ['dl'] + ['dl/%s' % n for n in range(1, 15)]
                     +
                     ['gw'] + ['gw/%s' % n for n in range(1, 40)],
            'pattern': '(?P<ip>(?:\d{1,3}\.){3}\d{1,3})</td>\n?\s*<td.*?>\s*(?P<port>\d{1,4})'
        },
        {
            'url': 'http://www.mimiip.com/%s',
            'range': ['%s/%s' % (m, n) for m in ['gngao', 'gnpu', 'gntou', 'hw'] for n in range(1, 5)],
            'pattern': '(?P<ip>(?:\d{1,3}\.){3}\d{1,3})</td>\n?\s*<td.*?>\s*(?P<port>\d{1,4})'
        },
    ]
    proxysites.extend(get_proxy_sites2())
    return proxysites


def get_proxy_sites2():
    import requests
    from bs4 import BeautifulSoup as BS
    from config import HEADER
    sites = []

    url = 'http://blog.kuaidaili.com/'
    pattern = '(?P<ip>(?:\d{1,3}\.){1,3}\d{1,3}):(?P<port>\d{1,4})'
    r = requests.get(url, headers=HEADER)
    if r.ok:
        soup = BS(r.content, 'lxml')
        for s in soup.find_all('article')[:2]:
            sites.append({
                'url': s.find('a')['href'],
                'range': [],
                'pattern': pattern
            })
    return sites
