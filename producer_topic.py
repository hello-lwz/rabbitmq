#-*- coding: UTF-8 -*-
import pika

credentials = pika.PlainCredentials('admin','password')
# 创建链接
connection = pika.BlockingConnection(pika.ConnectionParameters(
    'ip',5672,'/',credentials))
# 创建频道
channel = connection.channel()

# 创建模糊匹配类型的exchange
channel.exchange_declare(exchange='server',
                         exchange_type='topic')

routing_key = 'server'
# n RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange.
with open('test.yaml','r') as f:
    data = f.read()
channel.basic_publish(exchange='server',
                      routing_key=routing_key,
                      body=data)
print('---')
channel.close()
connection.close()
