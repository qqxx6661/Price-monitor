# -*- coding: utf-8 -*-
import mysql.connector
import time
import requests
from conn_sql import ItemQuery

if __name__ == '__main__':
    itemquery = ItemQuery()  # TODO： 第二轮无法继续抓取
    while (1):
        start = time.time()
        items = itemquery.read_itemid_temp()
        if itemquery.start_flag == 0:  # 非第一轮则继续使用上一轮代理
            print 'No previous round usable proxy'
            proxy = itemquery.use_proxy()
        for item in items:
            item_id = str(item[0])
            # item_id = item_id[1:-2]  # 现在啊同时获取用户和商品ID后不需要这条了
            user_id = str(item[1])
            mall_name = str(item[2])
            while (1):
                try:
                    item_name = itemquery.crawl_name(item_id, proxy, mall_name)
                    break
                except requests.exceptions.ReadTimeout:
                    proxy = itemquery.use_proxy()
                    localtime = time.asctime(time.localtime(time.time()))
                    print 'Read Timeout, change name proxy.', localtime
                    continue
                except requests.exceptions.ProxyError:
                    proxy = itemquery.use_proxy()
                    localtime = time.asctime(time.localtime(time.time()))
                    print 'Proxy Timeout, change name proxy.', localtime
                    continue
                except requests.exceptions.ConnectionError:
                    proxy = itemquery.use_proxy()
                    localtime = time.asctime(time.localtime(time.time()))
                    print 'Proxy Failure, change name proxy.', localtime
                    continue
                except IndexError:
                    proxy = itemquery.use_proxy()
                    localtime = time.asctime(time.localtime(time.time()))
                    print 'Proxy cannot get tb name, change name proxy.', localtime
                    continue
            while (1):
                try:
                    item_price = itemquery.crawl_price(item_id, proxy, mall_name)
                    break
                except requests.exceptions.ReadTimeout:
                    proxy = itemquery.use_proxy()
                    localtime = time.asctime(time.localtime(time.time()))
                    print 'Read Timeout, change price proxy.', localtime
                    continue
                except requests.exceptions.ProxyError:
                    proxy = itemquery.use_proxy()
                    localtime = time.asctime(time.localtime(time.time()))
                    print 'Proxy Timeout, change price proxy.', localtime
                    continue
                except requests.exceptions.ConnectionError:
                    proxy = itemquery.use_proxy()
                    localtime = time.asctime(time.localtime(time.time()))
                    print 'Proxy Failure, change price proxy.', localtime
                    continue
                except ValueError:
                    proxy = itemquery.use_proxy()
                    localtime = time.asctime(time.localtime(time.time()))
                    print 'Proxy cannot get jd price, change price proxy.', localtime
                    continue
                except IndexError:
                    proxy = itemquery.use_proxy()
                    localtime = time.asctime(time.localtime(time.time()))
                    print 'Proxy cannot get tb price, change price proxy.', localtime
                    continue
            itemquery.write_item_info(user_id, item_id, item_name, item_price)
            itemquery.compare_send_email(user_id, item_id, item_price, item_name)
            print '------------------------------------------------------------'
        # itemquery.conn.close()  # 由于conn为静态变量，此处不能关闭
        end = time.time()
        itemquery.start_flag = 1
        print 'Total time (sec)', end - start, 'Take a break for (sec): 3'
        time.sleep(3)
