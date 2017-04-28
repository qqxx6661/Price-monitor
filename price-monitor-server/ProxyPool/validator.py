#!/usr/bin/env python
# coding:utf-8
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
from logger import logger
import re
import time
import ipip
import requests
from ua import RandomHeader
from config import VALIDATE_CONFIG

requests.packages.urllib3.disable_warnings()
rh = RandomHeader()

class Validator:
    def __init__(self):
        self.http_target = VALIDATE_CONFIG['HTTP_TARGET']
        self.https_target = VALIDATE_CONFIG['HTTPS_TARGET']
        self.timeout = VALIDATE_CONFIG['TIMEOUT']
        self.thread_num = VALIDATE_CONFIG['THREAD_NUM']
        self.pattern = re.compile(
            r'((?:IP:Port)|(?:HTTP_CLIENT_IP)|(?:HTTP_X_FORWARDED_FOR))</td>\n?\s*<td.*?>(.*?)</td>', re.I)
        self.headers = rh.Header(self.http_target)
        self.ip = self._get_self_ip()
        self.IPL = ipip.IPL('17monipdb.dat')
        self.pool = Pool(self.thread_num)

    def run(self, proxies):
        # 采用gevent进行处理
        if not self.ip:
            logger.error('Validating fail, self ip is empty')
            return []
        avaliable_proxies = filter(lambda x: x, self.pool.map(self.validate, proxies))
        logger.info('Get %s avaliable proxies' % len(avaliable_proxies))
        return avaliable_proxies

    def _v(self, proxy, target):
        try:
            start = time.time()
            proxies = {
                'http': 'http://%s' % proxy,
                'https': 'http://%s' % proxy
            }
            r = requests.get(target, headers=self.headers, proxies=proxies, timeout=self.timeout, verify=False)
            if r.ok:
                speed = time.time() - start
                headers = self.pattern.findall(r.content)
                headers_info = {}
                for header in headers:
                    headers_info[header[0]] = header[1].split(':')[0]
                REMOTE_ADDR = headers_info.get('IP:Port', '')
                HTTP_VIA = headers_info.get('HTTP_CLIENT_IP', '')
                HTTP_X_FORWARDED_FOR = headers_info.get('HTTP_X_FORWARDED_FOR', '')
                if REMOTE_ADDR and REMOTE_ADDR != self.ip:
                    if not HTTP_X_FORWARDED_FOR:
                        if not HTTP_VIA:
                            type = 3
                    elif HTTP_X_FORWARDED_FOR != self.ip:
                        type = 2
                    else:
                        type = 1
                    logger.info('Validating %s, success, type:%s, time:%ss', proxy, type, speed)
                    return {
                        'ip': proxy.split(':')[0],
                        'port': proxy.split(':')[1],
                        'type': type,
                        'speed': speed,
                        'area': self.IPL.find(proxy.split(':')[0]).rstrip().replace('\t', '.')
                    }
        except Exception as e:
            logger.debug('Validating %s, fail: %s', proxy, e)
            pass
        return None

    def validate(self, (proxy, protocol)):
        proxy_info = None
        http_proxy_info = None
        https_proxy_info = None
        if protocol == 'http':
            http_proxy_info = self._v(proxy, self.http_target)
        if protocol == 'https':
            https_proxy_info = self._v(proxy, self.https_target)
        else:
            http_proxy_info = self._v(proxy, self.http_target)
            if not http_proxy_info:
                https_proxy_info = self._v(proxy, self.https_target)

        if http_proxy_info:
            http_proxy_info['protocol'] = 'http'
            proxy_info = http_proxy_info
        elif https_proxy_info:
            https_proxy_info['protocol'] = 'https'
            proxy_info = https_proxy_info
        return proxy_info

    def _get_self_ip(self):
        # 获取自身外网ip
        try:
            r = requests.get(self.http_target, headers=self.headers, timeout=5)
            if r.ok:
                pattern = re.compile(r'IP:port</td>\n?\s*<td.*?>([\d.]*?)(?::\d*)</td>', re.I)
                ip = pattern.search(r.content).group(1)
                logger.info('Get self ip success: %s' % ip)
                return ip
        except Exception, e:
            logger.warn('Get self ip fail, %s' % e)
            return ''
