# -*- coding: utf-8 -*-
import requests
import json
import re
from lxml import etree


class Crawl(object):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'}

    def get_price_jd(self, item_id_inner, proxy_inner):
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

    def get_name_jd(self, item_id_inner, proxy_inner):
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
                name = '本轮抓取该商品名称失败，请等待重试'
                return name
        return name  # 遇到return无需break了！

    def get_name_tb(self, item_id_inner, proxy_inner):
        url = 'https://item.taobao.com/item.htm?id=' + item_id_inner
        proxies = proxy_inner
        # print 'Use proxy:', proxies
        r = requests.get(url, headers=self.headers, proxies=proxies, timeout=6)
        selector = etree.HTML(r.text)
        name = selector.xpath("//*[@property='og:title']/@content")  # list
        print name
        if len(name) == 0:  # list长度为0
            return '本轮抓取该商品名称失败，请检查商品是否已下架，或者等待下轮重试'
        if name[0].strip == '':
            return '本轮抓取该商品名称失败，等待下轮重试'
        return name[0].strip()

    def get_price_tb(self, item_id_inner, proxy_inner):
        url = 'https://item.taobao.com/item.htm?id=' + item_id_inner
        proxies = proxy_inner
        # print 'Use proxy:', proxies
        r = requests.get(url, headers=self.headers, proxies=proxies, timeout=6)
        selector = etree.HTML(r.text)
        price = selector.xpath("//*[@class='tb-rmb-num']/text()")  # list
        print price  # list
        if not price[0].strip() == '':
            return price[0].strip()
        elif not price[3].strip() == '':
            return price[3].strip()
        else:
            return price[4].strip()

    def get_name_tm(self, item_id_inner, proxy_inner):
        url = 'https://detail.tmall.com/item.htm?id=' + item_id_inner
        proxies = proxy_inner
        # print 'Use proxy:', proxies
        r = requests.get(url, headers=self.headers, proxies=proxies, timeout=6)
        # print r.text
        selector = etree.HTML(r.text)
        name = selector.xpath("//*[@name='keywords']/@content")
        print name  # list
        if name[0].strip == '':
            return '本轮抓取该商品名称失败，请检查商品是否已下架，或者等待下轮重试'
        return name[0].strip()

    def get_price_tm(self, item_id_inner, proxy_inner):
        url = 'https://detail.tmall.com/item.htm?id=' + item_id_inner
        proxies = proxy_inner
        # print 'Use proxy:', proxies
        r = requests.get(url, headers=self.headers, proxies=proxies, timeout=6)
        # print r.text
        selector = etree.HTML(r.text)
        price = selector.xpath("//*[@id='J_DetailMeta']/div[1]/script[3]/text()")  # list
        price = re.findall(r'"defaultItemPrice":"(.*)"double', price[0])  # '699.00",'   list
        price = price[0][:-2]  # '699.00' 888.00-999.00需要正则，待修改, 下架商品, 待修改
        # print name[0], price
        return price