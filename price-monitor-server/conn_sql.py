# -*- coding: utf-8 -*-
import mysql.connector
from crawl import Crawl
from send_email import SendEmail
import time
import requests
import json


class ItemQuery(object):

    def read_itemid(self):
        cursor = conn.cursor()
        cursor.execute('select item_id, user_id from monitor where status=1')
        items_inner = cursor.fetchall()
        localtime = time.asctime(time.localtime(time.time()))
        print 'Local Time:', localtime
        print 'All item:', items_inner
        print '----------------------'
        cursor.close()
        return items_inner

    def crawl_name(self, item_id_inner, proxy_inner):
        crawl = Crawl()
        item_name_inner = crawl.get_name(item_id_inner, proxy_inner)
        return item_name_inner

    def crawl_price(self, item_id_inner, proxy_inner):
        crawl = Crawl()
        item_price_inner = crawl.get_price(item_id_inner, proxy_inner)
        return item_price_inner

    def write_item_info(self, user_id_inner, item_id_inner, item_name_inner, item_price_inner):
        cursor = conn.cursor()
        sql = 'update monitor set item_name = \'%s\', item_price = %s where item_id = %s and user_id = %s' % (item_name_inner, item_price_inner, item_id_inner, user_id_inner)
        print 'SQL update:', sql.encode('utf-8')  # ascii错误解决
        cursor.execute(sql)
        conn.commit()
        cursor.close()

    def compare_send_email(self, user_id_inner, item_id_inner, item_price_inner, item_name_inner):
        cursor = conn.cursor()
        sql = 'select user_price from monitor where item_id = %s and user_id = %s' % (item_id_inner, user_id_inner)
        print 'SQL query: ', sql
        cursor.execute(sql)
        user_price = cursor.fetchone()  # user_price: tuple, user_price[0]: decimal, item_price: unicode
        if float(user_price[0]) >= float(item_price_inner):  # 转为float才可以对比，可以改进
            try:
                sql = 'update monitor set status = 0 where item_id = %s and user_id = %s' % (item_id_inner, user_id_inner)
                cursor.execute(sql)
                conn.commit()
                sql = 'select user_email from user where user_id = %s' % user_id_inner
                cursor.execute(sql)
                user_email = cursor.fetchone()
                user_email = str(user_email[0])
                email_text = '您监控的商品：' + str(item_name_inner) + '，现在价格为：' + str(item_price_inner) + '，您设定的价格为：' + str(user_price[0]) + '  赶紧抢购吧！'
                email_text = email_text.encode('utf-8')
                email_zhuti = '您监控的商品降价了！'
                sendemail = SendEmail(email_text, 'admin', 'user', email_zhuti, user_email)
                sendemail.send()
                print '该商品降价，已发送邮件提醒用户'
            except UnicodeEncodeError as e:
                sql = 'update monitor set status = 1 where item_id = %s and user_id = %s' % (item_id_inner, user_id_inner)
                cursor.execute(sql)
                conn.commit()
                print '发送邮件过程中发生错误，等待下轮重试', e
        cursor.close()

    def use_proxy(self):
        while(1):
            url = 'http://localhost:8000/&type=3'
            r = requests.get(url, timeout=5)
            js = json.loads(r.text)
            try:    
                proxies_inner = {
                    'http': 'http://' + js[0],
                    'https': 'https://' + js[0],
                }
            except IndexError:
                print 'No proxy now, retrying'
                continue
            return proxies_inner

if __name__ == '__main__':
    while(1):
        start = time.time()
        conn = mysql.connector.connect(user='root', password='root', database='pricemonitor')
        query = ItemQuery()
        items = query.read_itemid()
        proxy = query.use_proxy()
        for item in items:
            item_id = str(item[0])
            # item_id = item_id[1:-2]  # 现在啊同时获取用户和商品ID后不需要这条了
            user_id = str(item[1])
            while(1):
                try:
                    item_name = query.crawl_name(item_id, proxy)
                    break
                except requests.exceptions.ReadTimeout:
                    print 'Read Timeout, change name proxy'
                    proxy = query.use_proxy()
                    continue
                except requests.exceptions.ProxyError:
                    print 'Proxy Timeout, change name proxy'
                    proxy = query.use_proxy()
                    continue
                except requests.exceptions.ConnectionError:
                    print 'Proxy Failure, change name proxy'
                    proxy = query.use_proxy()
                    continue
            while(1):
                try:
                    item_price = query.crawl_price(item_id, proxy)
                    break
                except requests.exceptions.ReadTimeout:
                    print 'Read Timeout, change price proxy'
                    proxy = query.use_proxy()
                    continue
                except requests.exceptions.ProxyError:
                    print 'Proxy Timeout, change price proxy'
                    proxy = query.use_proxy()
                    continue
                except requests.exceptions.ConnectionError:
                    print 'Proxy Failure, change price proxy'
                    proxy = query.use_proxy()
                    continue
                except ValueError:
                    print 'Proxy cannot get price, change price proxy'
                    proxy = query.use_proxy()
                    continue
            query.write_item_info(user_id, item_id, item_name, item_price)
            query.compare_send_email(user_id, item_id, item_price, item_name)
            print '------------------------------------------------------------'
        conn.close()
        end = time.time()
        print 'Total time(sec)', end - start
