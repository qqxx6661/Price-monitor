# -*- coding: utf-8 -*-
import requests
import json
from lxml import etree


# selector = etree.HTML(r.text)
# item_name = selector.xpath("//*[@class='sku-name']/text()")  # list
# item_name = item_name[0].strip()


class Crawl(object):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'}

    def get_price(self, item_id_inner):
        url = 'https://p.3.cn/prices/mgets?callback=&skuIds=J_' + item_id_inner
        r = requests.get(url, headers=self.headers)
        price = r.text
        price = price[2:-4]
        js = json.loads(str(price))
        return js['p']

    def get_name(self, item_id_inner):
        url = 'https://item.jd.com/' + item_id_inner + '.html'
        r = requests.get(url, headers=self.headers)
        selector = etree.HTML(r.text)
        name = selector.xpath("//*[@class='sku-name']/text()")  # list
        name = name[0].strip()
        return name

crawl = Crawl()
item_id = '2327501'
item_price = crawl.get_price(item_id)
item_name = crawl.get_name(item_id)
print item_name
print item_price
