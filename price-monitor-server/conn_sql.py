# -*- coding: utf-8 -*-
import mysql.connector
from crawl import Crawl
from send_email import SendEmail
import time
import requests
import json
import sys   #引用sys模块进来，并不是进行sys的第一次加载
reload(sys)  #重新加载sys
sys.setdefaultencoding('utf8')  ##调用setdefaultencoding函数

class ItemQuery(object):
    conn = mysql.connector.connect(user='root', password='root', database='pricemonitor')  # static variable
    start_flag = 0  # 记录是否为首轮
    def read_itemid(self):
        cursor = self.conn.cursor()
        cursor.execute('select item_id, user_id, mall_name from monitor where status=1')
        items_inner = cursor.fetchall()
        localtime = time.asctime(time.localtime(time.time()))
        print 'Local Time:', localtime
        print 'All item:', items_inner
        print '----------------------'
        cursor.close()
        return items_inner

    def read_itemid_temp(self):
        cursor = self.conn.cursor()
        cursor.execute('select item_id, user_id, mall_name from monitor where item_price is null and status = 1')
        items_inner = cursor.fetchall()
        localtime = time.asctime(time.localtime(time.time()))
        print 'Local Time:', localtime
        print 'All item:', items_inner
        print '----------------------'
        cursor.close()
        return items_inner

    def crawl_name(self, item_id_inner, proxy_inner, mall_name_inner):
        if mall_name_inner == 'jd':
            crawl = Crawl()
            item_name_inner = crawl.get_name_jd(item_id_inner, proxy_inner)
            return item_name_inner
        elif mall_name_inner == 'tm':
            #crawl = Crawl()
            #item_name_inner = crawl.get_name_tm(item_id_inner, proxy_inner)
            #return item_name_inner
            temp_item_name = '天猫价格抓取正在攻克中，名称暂不显示'
            return temp_item_name
        elif mall_name_inner == 'tb':
            #crawl = Crawl()
            #item_name_inner = crawl.get_name_tb(item_id_inner, proxy_inner)
            #return item_name_inner
            temp_item_name = '淘宝价格抓取正在攻克中，名称暂不显示'
            return temp_item_name
        else:
            return '该商品未设定商城名'

    def crawl_price(self, item_id_inner, proxy_inner, mall_name_inner):
        if mall_name_inner == 'jd':
            crawl = Crawl()
            item_price_inner = crawl.get_price_jd(item_id_inner, proxy_inner)
            return item_price_inner
        elif mall_name_inner == 'tm':
            #crawl = Crawl()
            #item_price_inner = crawl.get_price_tm(item_id_inner, proxy_inner)
            #return item_price_inner
            temp_item_price = '-1'
            return temp_item_price
        elif mall_name_inner == 'tb':
            #crawl = Crawl()
            #item_price_inner = crawl.get_price_tb(item_id_inner, proxy_inner)
            #return item_price_inner
            temp_item_price = '-1'
            return temp_item_price
        else:
            return '-1'

    def write_item_info(self, user_id_inner, item_id_inner, item_name_inner, item_price_inner):
        cursor = self.conn.cursor()
        sql = 'update monitor set item_name = \'%s\', item_price = %s where item_id = %s and user_id = %s' % (item_name_inner, item_price_inner, item_id_inner, user_id_inner)
        print 'SQL update:', sql.encode('utf-8')  # ascii错误解决，不加的话控制台中文乱码, 记得添加回去
        cursor.execute(sql)
        self.conn.commit()
        cursor.close()

    def compare_send_email(self, user_id_inner, item_id_inner, item_price_inner, item_name_inner):
        cursor = self.conn.cursor()
        try:
            sql = 'select user_price from monitor where item_id = %s and user_id = %s' % (item_id_inner, user_id_inner)
            # print 'SQL query: ', sql
            cursor.execute(sql)
            user_price = cursor.fetchone()  # user_price: tuple, user_price[0]: decimal, item_price: unicode
        except mysql.connector.errors.InternalError:
            note = '拥有重复商品，每个商品只能有一个监控，否则会导致监控失败。'
            sql = 'update monitor set note = \'%s\' where item_id = %s and user_id = %s' % (note, item_id_inner, user_id_inner)
            print 'Have same item id in one user, skip this round.'
            cursor.execute(sql)
            self.conn.commit()
            cursor.close()
            return
        if float(item_price_inner) == -1.00:  # 抓取到-1不发邮件，状态依然为1
            note = '商品已经下架或者ID不正确。'
            sql = 'update monitor set note = \'%s\' where item_id = %s and user_id = %s' % (note, item_id_inner, user_id_inner)
            print 'Wrong item price: -1, skip this round.'
            cursor.execute(sql)
            self.conn.commit()
            cursor.close()
            return
        if float(user_price[0]) >= float(item_price_inner):  # 转为float才可以对比，可以改进
            # try:
            sql = 'update monitor set status = 0 where item_id = %s and user_id = %s' % (item_id_inner, user_id_inner)
            cursor.execute(sql)
            self.conn.commit()
            sql = 'select user_email from user where user_id = %s' % user_id_inner
            cursor.execute(sql)
            user_email = cursor.fetchone()
            user_email = str(user_email[0])  # linux可用，win会报下面的错误
            # item_url = 'https://item.jd.com/' + item_id_inner + '.html'  # 邮件网址，怀疑是垃圾邮件原因
            email_text = '您监控的商品：' + item_name_inner + '，' + '，现在价格为：' + item_price_inner + '，您设定的价格为：' + str(user_price[0]) + '  赶紧抢购吧！'.encode('utf-8')
            email_text = email_text
            email_zhuti = '您监控的商品降价了！'
            sendemail = SendEmail(email_text, 'admin', 'user', email_zhuti, user_email)
            sendemail.send()
            print '该商品降价，已发送邮件提醒用户'
            '''
            except UnicodeEncodeError as e:
                sql = 'update monitor set status = 1 where item_id = %s and user_id = %s' % (item_id_inner, user_id_inner)
                cursor.execute(sql)
                self.conn.commit()
                print '发送邮件过程中发生错误，等待下轮重试，正在监控状态继续', e
            except UnicodeDecodeError as e:
                sql = 'update monitor set status = 1 where item_id = %s and user_id = %s' % (item_id_inner, user_id_inner)
                cursor.execute(sql)
                self.conn.commit()
                print '发送邮件过程中发生错误，等待下轮重试，正在监控状态继续', e
            '''
        cursor.close()

    def use_proxy(self):
        while(1):
            url = 'http://localhost:8000/&type=3'
            try:
                r = requests.get(url, timeout=5)
                js = json.loads(r.text)
                proxies_inner = {
                    'http': 'http://' + js[0],
                    'https': 'https://' + js[0],
                }
            except IndexError:
                print 'No usable proxy now, retrying'
                time.sleep(5)
                continue
            except requests.exceptions.ConnectionError:
                print 'No proxy now, retrying'
                time.sleep(5)
                continue
            except requests.exceptions.ReadTimeout:
                print 'No proxy now, retrying'
                time.sleep(5)
                continue
            return proxies_inner

    def start_monitor(self, break_time):
        while (1):
            start = time.time()
            query = ItemQuery()
            items = query.read_itemid()
            if self.start_flag == 0:  # 非第一轮则继续使用上一轮代理
                print 'No previous round usable proxy'
                proxy = query.use_proxy()
            for item in items:
                item_id = str(item[0])
                # item_id = item_id[1:-2]  # 现在同时获取用户和商品ID后不需要这条了
                user_id = str(item[1])
                mall_name = str(item[2])
                while (1):
                    try:
                        item_name = query.crawl_name(item_id, proxy, mall_name)
                        break
                    except requests.exceptions.ReadTimeout:
                        proxy = query.use_proxy()
                        localtime = time.asctime(time.localtime(time.time()))
                        print 'Read Timeout, change name proxy.', localtime
                        continue
                    except requests.exceptions.ProxyError:
                        proxy = query.use_proxy()
                        localtime = time.asctime(time.localtime(time.time()))
                        print 'Proxy Timeout, change name proxy.', localtime
                        continue
                    except requests.exceptions.ConnectionError:
                        proxy = query.use_proxy()
                        localtime = time.asctime(time.localtime(time.time()))
                        print 'Proxy Failure, change name proxy.', localtime
                        continue
                    except requests.exceptions.ContentDecodingError:
                        proxy = query.use_proxy()
                        localtime = time.asctime(time.localtime(time.time()))
                        print 'Proxy Failure, change name proxy.', localtime
                        continue
                    except requests.exceptions.ChunkedEncodingError:
                        proxy = query.use_proxy()
                        localtime = time.asctime(time.localtime(time.time()))
                        print 'Proxy Failure, change name proxy.', localtime
                        continue
                    except IndexError:
                        proxy = query.use_proxy()
                        localtime = time.asctime(time.localtime(time.time()))
                        print 'Proxy cannot get tb name, change name proxy.', localtime
                        continue
                while (1):
                    try:
                        item_price = query.crawl_price(item_id, proxy, mall_name)
                        break
                    except requests.exceptions.ReadTimeout:
                        proxy = query.use_proxy()
                        localtime = time.asctime(time.localtime(time.time()))
                        print 'Read Timeout, change price proxy.', localtime
                        continue
                    except requests.exceptions.ProxyError:
                        proxy = query.use_proxy()
                        localtime = time.asctime(time.localtime(time.time()))
                        print 'Proxy Timeout, change price proxy.', localtime
                        continue
                    except requests.exceptions.ConnectionError:
                        proxy = query.use_proxy()
                        localtime = time.asctime(time.localtime(time.time()))
                        print 'Proxy Failure, change price proxy.', localtime
                        continue
                    except ValueError:
                        proxy = query.use_proxy()
                        localtime = time.asctime(time.localtime(time.time()))
                        print 'Proxy cannot get jd price, change price proxy.', localtime
                        continue
                    except IndexError:
                        proxy = query.use_proxy()
                        localtime = time.asctime(time.localtime(time.time()))
                        print 'Proxy cannot get tb price, change price proxy.', localtime
                        continue
                query.write_item_info(user_id, item_id, item_name, item_price)
                query.compare_send_email(user_id, item_id, item_price, item_name)
                print '------------------------------------------------------------'
            # self.conn.close()  # 由于conn为静态变量，此处不能关闭
            end = time.time()
            self.start_flag = 1
            print 'Total time (sec)', end - start, 'Take a break for (sec):', break_time
            time.sleep(break_time)

if __name__ == '__main__':
    itemquery = ItemQuery()
    itemquery.start_monitor(30)

