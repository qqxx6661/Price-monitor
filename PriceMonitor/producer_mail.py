import json
import logging

import pika

from CONFIG import RABBIT_MQ_HOST


class ProducerMail:

    @staticmethod
    def send_mail_message(data):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_MQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue='mail')

        channel.basic_publish(exchange='', routing_key='mail', body=json.dumps(data))
        connection.close()


if __name__ == '__main__':
    logging.basicConfig(format="%(asctime)s | %(levelname)s | %(filename)s %(lineno)s | %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        level=logging.INFO)
    data = {'subject': "【主题】", 'address': "xxxxxxxx@foxmail.com", 'msg': "内容", 'from': "发送者", 'to': "接收者", "id": 1}
    ProducerMail.send_mail_message(data)
