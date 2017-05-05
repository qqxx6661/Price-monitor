# -*- coding: utf-8 -*-
import requests
import json
from lxml import etree

class Crawl(object):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'}

    def get_price(self, item_id_inner, proxy_inner):
        url = 'https://p.3.cn/prices/mgets?callback=&skuIds=J_' + item_id_inner
        # print '该商品价格URL：', url
        proxies = proxy_inner
        # print 'Use proxy:', proxies
        r = requests.get(url, headers=self.headers, proxies=proxies, timeout=6)
        price = r.text
        if price == 'skuids input error\n':  # 防止瞎填商品ID导致无法继续爬
            js_fake = '-1'
            return js_fake
        price = price[2:-4]
        js = json.loads(str(price))
        print 'JS price:', js
        return js['p']

    def get_name(self, item_id_inner, proxy_inner):
        url = 'https://item.jd.com/' + item_id_inner + '.html'
        proxies = proxy_inner
        # print 'Use proxy:', proxies
        r = requests.get(url, headers=self.headers, proxies=proxies, timeout=6)
        selector = etree.HTML(r.text)
        name = selector.xpath("//*[@class='sku-name']/text()")  # list
        try:
            name = name[0].strip()
        except IndexError as e:
            print e, name
            print 'Change method to catch name'
            try:
                name = selector.xpath("//*[@id='name']/h1/text()")
                name = name[0].strip()
            except IndexError as e:
                print e, name
                print 'Catch name error'
                name = '本次抓取该商品名称失败，请检查商品ID'
                return name
        return name  # 遇到return无需break了！


if __name__ == '__main__':
    pass