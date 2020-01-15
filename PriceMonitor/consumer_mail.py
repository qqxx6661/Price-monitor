import json
import logging

import pika

from CONFIG import RABBIT_MQ_HOST
from database.sql_operator import SqlOperator

from PriceMonitor.mail import Mail


class ConsumerJdCrawl:
    sql_operator = None

    def __init__(self):

        # 数据库连接初始化
        self.sql_operator = SqlOperator()
        # 订阅频道
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_MQ_HOST))
        channel = connection.channel()
        # 如果确定已经声明了，可以不声明。但是你不知道消费者生产者哪个先运行，所以要声明两次。
        channel.queue_declare(queue='mail')
        channel.basic_consume('mail', self.callback)
        logging.info('开始监听Queue：mail')
        channel.start_consuming()

    def callback(self, ch, method, properties, body):  # 四个参数为标准格式
        logging.info("收到消息: %r 序号为：%r" % (body, method.delivery_tag))
        self.thread_run(ch, method, body)

    def thread_run(self, ch, method, body):
        logging.info("线程开始处理消息： %r 序号为：%r" % (body, method.delivery_tag))
        data = json.loads(body)
        # 再次确认是否需要发邮件，防止并发爬虫检查都为0
        is_email_needed = self.sql_operator.query_email_alert_needed(data["id"])
        if not is_email_needed:
            logging.info("发送邮件前检查is_alert状态为0，不需要重复提醒： %r" % method.delivery_tag)
            logging.info("消息不作发送邮件处理，发送确认序号： %r" % method.delivery_tag)
            return
        logging.info("发送邮件：", data)
        send_email = Mail(data["msg"], data["from"], data["to"], data["subject"], data["address"])
        is_sent = send_email.send()
        # 将数据库alert改为0
        if is_sent:
            self.sql_operator.update_alert_info(data["id"], 0)
        # delivery_tag是确认序号
        logging.info("消息处理完成，发送确认序号： %r" % method.delivery_tag)
        ch.basic_ack(delivery_tag=method.delivery_tag)



if __name__ == '__main__':
    logging.basicConfig(format="%(asctime)s | %(levelname)s | %(filename)s %(lineno)s | %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        level=logging.INFO)
    thread = ConsumerJdCrawl()
