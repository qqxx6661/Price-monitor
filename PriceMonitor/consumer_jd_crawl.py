import json
import logging
import os
import time

import pika

from CONFIG import RABBIT_MQ_HOST, SELENIUM_THREAD
from crawler_selenium import Crawler
from database.sql_operator import SqlOperator
from producer_mail import ProducerMail


class ConsumerJdCrawl:
    sql_operator = None
    executor = None

    def __init__(self):

        # 数据库连接初始化
        self.sql_operator = SqlOperator()
        # 订阅频道
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_MQ_HOST))
        channel = connection.channel()
        # 如果确定已经声明了，可以不声明。但是你不知道消费者生产者哪个先运行，所以要声明两次。
        channel.queue_declare(queue='jd_crawl')
        # prefetch_count 如果消费者中有一条消息没有处理完，就不会继续给这个消费者发送新消息
        channel.basic_qos(prefetch_count=SELENIUM_THREAD)
        channel.basic_consume('jd_crawl', self.callback)
        logging.info('开始监听Queue：jd_crawl')
        channel.start_consuming()

    def callback(self, ch, method, properties, body):  # 四个参数为标准格式
        logging.info("收到消息: %r 序号为：%r" % (body, method.delivery_tag))
        self.thread_run(ch, method, body)

    def thread_run(self, ch, method, body):
        logging.info("线程开始处理消息： %r 序号为：%r" % (body, method.delivery_tag))
        # 爬取商品
        # crawl_data:{'id': "1532", 'item_id': "4749125"}
        try:
            crawl_data = json.loads(body)
        except BaseException:
            logging.info("消息结构不对，丢弃，发送确认序号： %r" % method.delivery_tag)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
        item_info, huihui_info = self.jd_crawl(crawl_data)
        # 存入数据库
        self.sql_operator.update_pm_monitor_item(crawl_data, item_info, huihui_info)
        # 确认是否需要邮件发送，若是则发送邮件到消息队列
        is_email_needed = self.sql_operator.query_email_alert_needed(crawl_data["id"])
        if is_email_needed:
            logging.info("需要发送邮件提醒，pm_monitor_id：[{}]".format(crawl_data["id"]))
            # 获取用户信息
            user_info = self.sql_operator.query_user_info(crawl_data["id"])
            item_info_all = self.sql_operator.query_pm_monitor_item(crawl_data["id"])
            # 调用发送邮件队列
            self.mail_fill(user_info, item_info_all)
        # delivery_tag是确认序号
        logging.info("消息处理完成，发送确认序号： %r" % method.delivery_tag)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def jd_crawl(self, crawl_data):
        """
        爬取京东商品数据和慧慧最高最低价数据
        """
        logging.info("开始爬取：{}".format(crawl_data))
        start = time.time()
        item_info, huihui_info = self.crawl(crawl_data)
        end = time.time()
        logging.info("爬虫执行时间: {}".format(end - start))
        return item_info, huihui_info

    @staticmethod
    def mail_fill(user_info, item_info):
        """
        填充邮件内容
        """
        logging.info("开始撰写提醒邮件内容")
        if not item_info.min_price:
            item_info.min_price = '暂无历史最低价格'
            item_info.max_price = '暂无历史最高价格'
        item_url = 'https://item.jd.com/' + str(item_info.item_id) + '.html'
        email_text = '监控更新，增加会员监控功能，未来将努力打造为一站式监控平台，欢迎提需求和建议。\n\n'
        if not item_info.last_price:
            email_text += '物品：' + item_info.name + '，\n现在价格为：' + str(item_info.price) + \
                          '\n您设定的价格为： ' + str(item_info.user_price) + '\n子标题：' + item_info.subtitle + \
                          '\n历史最高价参考（不准确参考）：' + str(item_info.max_price) + '\n历史最低价参考（不准确参考）：' + str(item_info.min_price) + \
                          '\n' + item_url + '\n\n\n'
        else:
            email_text += '物品：' + item_info.name + '，\n上次监控价格为：' + str(item_info.last_price) + \
                          '，\n现在价格为：' + str(item_info.price) + '\n您设定的价格为： ' + str(item_info.user_price) + \
                          '\n降价幅度为：' + str(round(10 * float(item_info.discount), 2)) + '折，赶紧购买吧！' + \
                          '\n子标题：' + item_info.subtitle + '\n历史最高价参考（不准确参考）：' + str(item_info.max_price) + \
                          '\n历史最低价参考（不准确参考）：' + str(item_info.min_price) + '\n' + item_url + '\n\n\n'
        email_subject = '【电商价格监控】设定商品降价通知'

        data = dict()
        data["msg"] = email_text
        data["from"] = '电商价格监控'
        data["to"] = '注册用户'
        data["subject"] = email_subject
        data["address"] = user_info["email"]
        data["id"] = item_info.id
        ProducerMail.send_mail_message(data)
        logging.info("提醒邮件已经发送进队列")

    @staticmethod
    def crawl(crawl_data):
        retry = 2
        item_info = {"name": None, "price": None, "plus_price": None, "subtitle": None}
        while retry:
            try:
                crawler_jd = Crawler()
                # dict: {"name", "price", "subtitle", "plus_price"}
                item_info = crawler_jd.get_jd_item(str(crawl_data["item_id"]))
                crawler_jd.close()
            except ConnectionResetError:
                retry -= 1
                logging.warning('proxy connection reset by peer，delete proxy and retrying: {} left.'.format(retry))
                continue
            if not item_info["price"]:
                retry -= 1
                logging.warning('Cannot get item price，delete proxy and retrying: {} left.'.format(retry))
                continue
            else:
                break
        crawler_huihui = Crawler()
        # dict: {"max_price", "min_price"}
        huihui_info = crawler_huihui.get_huihui_item(str(crawl_data["item_id"]))
        crawler_huihui.close()
        return item_info, huihui_info

if __name__ == '__main__':
    logging.basicConfig(format="%(asctime)s | %(levelname)s | %(filename)s %(lineno)s | %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        level=logging.INFO)
    thread = ConsumerJdCrawl()
