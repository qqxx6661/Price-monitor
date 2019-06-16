#!/usr/bin/env python3
# coding=utf-8
import requests
import json
from lxml import etree
import logging


class Crawler(object):

    @staticmethod
    def get_info_huihui(item_id, header, proxy=None):
        url = 'https://zhushou.huihui.cn/productSense?phu=https://item.jd.com/' + item_id + '.html'
        logging.debug('Ready to crawl huihui price URL：%s', url)
        try:
            if proxy:  # Using proxy
                proxies = proxy
                r = requests.get(url, headers=header, proxies=proxies, timeout=5)
            else:  # Not using proxy
                logging.info('Not using proxy to crawl huihui')
                r = requests.get(url, headers=header, timeout=5)
            max_price = r.json()['max']
            min_price = r.json()['min']
            logging.info('max and min price: %s, %s', max_price, min_price)
            return max_price, min_price

        except requests.exceptions.ProxyError as e:
            logging.info('Proxy error: %s', e)
            return False
        except requests.exceptions.ConnectionError as e:
            logging.info('Https error: %s', e)
            return False
        except requests.exceptions.ReadTimeout as e:
            logging.info('Timeout error: %s', e)
            return False
        except requests.exceptions.ChunkedEncodingError as e:
            logging.info('ChunkedEncodingError error: %s', e)
            return False

    @staticmethod
    def get_subtitle_jd(item_id, header, proxy=None):
        url = 'https://cd.jd.com/promotion/v2?callback=jQuery6525446&skuId=' + item_id + \
              '5181380&area=1_72_2799_0&shopId=1000000904&venderId=1000000904&cat=9987%2C653%2C655'
        logging.debug('Ready to crawl jd subtitle URL：%s', url)
        try:
            if proxy:  # Using proxy
                proxies = proxy
                r = requests.get(url, headers=header, proxies=proxies, timeout=5)
            else:  # Not using proxy
                logging.info('Not using proxy to crawl subtitle')
                r = requests.get(url, headers=header, timeout=5)
            subtitle = r.text
            try:
                subtitle = subtitle[14:-1]
                print(subtitle)
                subtitle_js = json.loads(str(subtitle))
            except json.decoder.JSONDecodeError as e:
                logging.info('Captcha error: %s', e)
                return False
            logging.info('subtitle: %s, %s', subtitle)
            return subtitle_js['ads'][0]['ad']
        except requests.exceptions.ProxyError as e:
            logging.info('Proxy error: %s', e)
            return False
        except requests.exceptions.ConnectionError as e:
            logging.info('Https error: %s', e)
            return False
        except requests.exceptions.ReadTimeout as e:
            logging.info('Timeout error: %s', e)
            return False
        except requests.exceptions.ChunkedEncodingError as e:
            logging.info('ChunkedEncodingError error: %s', e)
            return False

    @staticmethod
    def get_price_jd(item_id, header, proxy=None):
        url = 'https://p.3.cn/prices/mgets?callback=&skuIds=J_' + item_id
        logging.debug('Ready to crawl JD price URL：%s', url)
        try:
            if proxy:  # Using proxy
                proxies = proxy
                r = requests.get(url, headers=header, proxies=proxies, timeout=5)
            else:  # Not using proxy
                logging.info('Not using proxy to crawl price')
                r = requests.get(url, headers=header, timeout=5)
            price = r.text
            # can not use status code because wrong id also get 200
            if price == 'skuids input error\n':  # Avoid invalid item id
                js_fake = '-1'
                return js_fake
            try:
                price = price[2:-4]
                price_js = json.loads(str(price))
            except json.decoder.JSONDecodeError as e:
                logging.info('Captcha error: %s', e)
                return False
            logging.info('Item: %s ,price JS: %s', item_id, price_js)
            return price_js['p']
        except requests.exceptions.ProxyError as e:
            logging.info('Proxy error: %s', e)
            return False
        except requests.exceptions.ConnectionError as e:
            logging.info('Https error: %s', e)
            return False
        except requests.exceptions.ReadTimeout as e:
            logging.info('Timeout error: %s', e)
            return False
        except requests.exceptions.ChunkedEncodingError as e:
            logging.info('ChunkedEncodingError error: %s', e)
            return False

    @staticmethod
    def get_name_jd(item_id, header, proxy=None):
        url = 'https://item.jd.com/' + item_id + '.html'
        logging.debug('Ready to crawl JD name URL：%s', url)
        try:
            if proxy:  # Using proxy
                logging.info('Using proxy to crawl: %s', proxy)
                r = requests.get(url, headers=header, proxies=proxy, timeout=6)
            else:  # Not using proxy
                logging.info('Not using proxy to crawl name')
                r = requests.get(url, headers=header, timeout=6)
            selector = etree.HTML(r.text)
            name = selector.xpath("//*[@class='sku-name']/text()")  # list
            try:  # normal
                name_true = name[0].strip()
                if not len(name_true):  # jd chaoshi
                    logging.info('Change method to catch name: jd chaoshi')
                    name_true = name[1].strip()
            except IndexError as e:
                logging.info(e, name)
                logging.info('Change method to catch name: jd jingxuan')
                try:  # jd jingxuan
                    name = selector.xpath("//*[@id='name']/h1/text()")
                    name_true = name[0].strip()
                except IndexError as e:
                    logging.warning(e, name)
                    logging.warning('Catch name error')
                    name_true = '本轮抓取该商品名称失败，请等待重试'
                    return name_true
            logging.info('Item: %s', name_true)
            return name_true
        except requests.exceptions.ProxyError as e:
            logging.info('Proxy error: %s', e)
            return ''  # as False
        except requests.exceptions.ConnectionError as e:
            logging.info('Https error: %s', e)
            return ''  # as False
        except requests.exceptions.ReadTimeout as e:
            logging.info('Timeout error: %s', e)
            return ''  # as False
        except requests.exceptions.ChunkedEncodingError as e:
            logging.info('ChunkedEncodingError error: %s', e)
            return ''  # as False


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    c = Crawler()
    # logging.debug(c.get_price_jd('2777811', {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
    #                                                    'AppleWebKit/536.6 (KHTML, like Gecko) '
    #                                                    'Chrome/20.0.1092.0 Safari/536.6'}))
    # logging.debug(c.get_name_jd('2777811', {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
    #                                                       'AppleWebKit/536.6 (KHTML, like Gecko) '
    #                                                       'Chrome/20.0.1092.0 Safari/536.6'}))
    # logging.debug(c.get_subtitle_jd('5181380', {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
    #                                                       'AppleWebKit/536.6 (KHTML, like Gecko) '
    #                                                       'Chrome/20.0.1092.0 Safari/536.6'}))
    # logging.debug(c.get_info_huihui('2777811', {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
    #                                                           'AppleWebKit/536.6 (KHTML, like Gecko) '
    #                                                           'Chrome/20.0.1092.0 Safari/536.6'}))
