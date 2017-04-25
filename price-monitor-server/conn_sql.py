# -*- coding: utf-8 -*-
import mysql.connector
from crawl import Crawl
from send_email import SendEmail
import sys
reload(sys)
sys.setdefaultencoding("utf-8")  # 不加入的话邮件发送会报编码错误

class ItemQuery(object):

    def read_itemid(self):
        cursor = conn.cursor()
        cursor.execute('select item_id from monitor where status=1')
        items_inner = cursor.fetchall()
        print '待查询的商品ID：', items_inner
        cursor.close()
        return items_inner

    def crawl_name_price(self, item_id):
        crawl = Crawl()
        item_price_inner = crawl.get_price(item_id)
        item_name_inner = crawl.get_name(item_id)
        return item_name_inner, item_price_inner

    def write_item_info(self, item_id, item_name_inner, item_price_inner):
        item_name_inner = '\'' + item_name_inner + '\''  # sql插入varchar前后有引号，可以改进
        cursor = conn.cursor()
        sql = 'update monitor set item_name = %s, item_price = %s where item_id = %s' % (item_name_inner, item_price_inner, item_id)
        print '更新语句为：', sql
        cursor.execute(sql)
        conn.commit()
        cursor.close()

    def compare_send_email(self, item_id, item_price_inner, item_name_inner):
        cursor = conn.cursor()
        sql = 'select user_price from monitor where item_id = %s' % item_id
        print '查询语句为：', sql
        cursor.execute(sql)
        user_price = cursor.fetchone()  # user_price: tuple user_price[0]: decimal item_price: unicode
        if float(user_price[0]) >= float(item_price_inner):  # 转为float才可以对比，可以改进
            sql = 'update monitor set status = 0 where item_id = %s' % item_id
            cursor.execute(sql)
            conn.commit()
            sql = 'select user_email from user where user_id = ( select user_id from monitor where item_id = %s )' % item_id
            cursor.execute(sql)
            user_email = cursor.fetchone()
            user_email = str(user_email[0])  # 改进
            email_text = '您监控的商品：' + str(item_name_inner) + '，现在价格为：' + str(item_price_inner) + '，您设定的价格为：' + str(user_price[0]) + '赶紧抢购吧！'
            email_zhuti = '您监控的商品降价了！'
            sendemail = SendEmail(email_text, 'admin', 'user', email_zhuti, user_email)
            sendemail.send()
            print '该商品降价，已发送邮件提醒用户'
        cursor.close()


conn = mysql.connector.connect(user='root', password='root', database='price-monitor')
query = ItemQuery()
items = query.read_itemid()
for item in items:
    item = str(item)  # 可以改进,items为tuple
    item = item[1:-2]
    item_name, item_price = query.crawl_name_price(item)
    query.write_item_info(item, item_name, item_price)
    query.compare_send_email(item, item_price, item_name)
conn.close()
