# -*- coding: utf-8 -*-
import requests
import json
from lxml import etree

class Crawl(object):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'}

    def get_price(self, item_id_inner):
        url = 'https://p.3.cn/prices/mgets?callback=&skuIds=J_' + item_id_inner
        print '该商品价格URL：', url
        while(True):
            proxies = self.use_proxy()
            print '本次使用：', proxies
            try:
                r = requests.get(url, headers=self.headers, proxies=proxies, timeout=10)
            except requests.exceptions.ProxyError as e:
                print '超时，重新更换代理', e
                continue
            except requests.exceptions.ConnectionError as e:
                print '代理失效，重新获取代理', e
                continue
            price = r.text
            price = price[2:-4]
            try:
                js = json.loads(str(price))
                print '价格js为：', js
                return js['p']
            except ValueError as e:
                print '该代理获取价格失败，重新获取代理', e
                continue

    def get_name(self, item_id_inner):
        url = 'https://item.jd.com/' + item_id_inner + '.html'
        while(True):
            proxies = self.use_proxy()
            print '本次使用：', proxies
            try:
                r = requests.get(url, headers=self.headers, proxies=proxies, timeout=10)
            except requests.exceptions.ProxyError as e:
                print '超时，重新获取代理', e
                continue
            except requests.exceptions.ConnectionError as e:
                print '代理失效，重新获取代理', e
                continue
            except requests.exceptions.SSLError as e:
                print '代理需要SSL，重新更换代理', e
                continue
            selector = etree.HTML(r.text)
            name = selector.xpath("//*[@class='sku-name']/text()")  # list
            try:
                name = name[0].strip()
            except IndexError as e:
                print e
                print '尝试第二种名称捕获方式'
                try:
                    name = selector.xpath("//*[@id='name']/h1/text()")
                    name = name[0].strip()
                except IndexError as e:
                    print e
                    print '名称捕获失败'
            return name  # 遇到return无需break了！

    def use_proxy(self):
        while(True):
            url = 'http://localhost:8000/&type=3'
            try:
                r = requests.get(url, headers=self.headers, timeout=5)
            except:
                continue
            js = json.loads(r.text)
            proxies_inner = {
                'http': 'http://' + js[0],
                'https': 'https://' + js[0],
            }
            return proxies_inner


if __name__ == '__main__':
    crawl = Crawl()
    proxies_test = crawl.use_proxy()
    print proxies_test
