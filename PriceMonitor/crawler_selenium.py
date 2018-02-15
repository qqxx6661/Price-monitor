#!/usr/bin/env python3
# coding=utf-8
from gevent import monkey  # IMPORT: must import gevent at first
monkey.patch_all()
import logging
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
import time
import json


class Crawler(object):

    def __init__(self, proxy=None):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        if proxy:
            proxy_address = proxy['https']
            chrome_options.add_argument('--proxy-server=%s' % proxy_address)
            logging.info('Chrome using proxy: %s', proxy['https'])
        self.chrome = webdriver.Chrome(chrome_options=chrome_options)
        # wait 3 seconds for start session (may delete)
        self.chrome.implicitly_wait(5)
        # set timeout like requests.get()
        # jd sometimes load google pic takes much time
        self.chrome.set_page_load_timeout(60)
        # set timeout for script
        self.chrome.set_script_timeout(60)

    def get_jd_item(self, item_id):
        item_info = ()
        # url = 'http://httpbin.org/ip'
        url = 'https://item.jd.com/' + item_id + '.html'
        try:
            self.chrome.get(url)
            # print('source', self.chrome.page_source)
            name = self.chrome.find_element_by_xpath("//*[@class='sku-name']").text
            price = self.chrome.find_element_by_xpath("//*[@class='p-price']").text
            subtitle = self.chrome.find_element_by_xpath("//*[@id='p-ad']").text
            plus_price = self.chrome.find_element_by_xpath("//*[@class='p-price-plus']").text  # may get null
            item_info = (name, price[1:], subtitle, plus_price[1:])
            logging.info('Crawl SUCCESS: %s', item_info)
        except NoSuchElementException as e:
            logging.warning('Crawl failure: %s', e)
        except TimeoutException as e:
            logging.warning('Crawl failure: %s', e)
        self.chrome.quit()
        return item_info

    def get_huihui_item(self, item_id):
        huihui_info = ()
        url = 'https://zhushou.huihui.cn/productSense?phu=https://item.jd.com/' + item_id + '.html'
        try:
            self.chrome.get(url)
            url_text = self.chrome.find_element_by_tag_name('body').text
            # print('source', url_text)
            info = json.loads(url_text)
            max_price = info['max']
            min_price = info['min']
            logging.info('max and min price: %s, %s', max_price, min_price)
            huihui_info = (max_price, min_price)
        except NoSuchElementException as e:
            logging.warning('Crawl failure: %s', e)
        except TimeoutException as e:
            logging.warning('Crawl failure: %s', e)
        self.chrome.quit()
        return huihui_info

    def get_cate_item(self, url):
        item_infos = []
        try:
            self.chrome.get(url)
            item_names = self.chrome.find_elements_by_xpath("//*[@class='gl-item']/div/div[4]/a/em")
            item_subtitles = self.chrome.find_elements_by_xpath("//*[@class='gl-item']/div/div[4]/a")
            item_prices = self.chrome.find_elements_by_xpath("//*[@class='gl-item']/div/div[3]/strong[1]/i")
            item_ids = self.chrome.find_elements_by_xpath("//*[@class='gl-item']/div/div[6]/a")
            for i in range(len(item_names)):
                item_infos.append([item_ids[i].get_attribute('data-sku'),
                                   item_names[i].text, item_prices[i].text, item_subtitles[i].get_attribute('title')])
            logging.info('item_infos: {}'.format(item_infos))
        except StaleElementReferenceException as e:
            logging.warning('Crawl failure: %s', e)
        except NoSuchElementException as e:
            logging.warning('Crawl failure: %s', e)
        except TimeoutException as e:
            logging.warning('Crawl failure: %s', e)
        self.chrome.quit()
        return item_infos


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start = time.time()
    c = Crawler()
    # c = Crawler({'http': '125.105.32.168:7305', 'https': '171.211.32.79:2456'})
    # logging.debug(c.get_jd_item('2777811'))
    logging.debug(c.get_huihui_item('2777811'))
    # logging.debug(c.get_cate_item('https://list.jd.com/list.html?cat=9987,653,655&page=2'
    #                               '&sort=sort_rank_asc&trans=1&JL=6_0_0&ms=6#J_main'))
    end = time.time()
    print(end-start)
