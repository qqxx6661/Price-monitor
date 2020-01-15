import json
import pika

from CONFIG import RABBIT_MQ_HOST

connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_MQ_HOST))
channel = connection.channel()
channel.queue_declare(queue='jd_crawl')

data = {'id': "1", 'item_id': "100008348542"}

channel.basic_publish(exchange='', routing_key='jd_crawl', body=json.dumps(data))
connection.close()
