#-*- coding: UTF-8 -*-
import pika

credentials = pika.PlainCredentials('admin','password')
# 创建链接
connection = pika.BlockingConnection(pika.ConnectionParameters(
    'ip',5672,'/',credentials))
# 创建频道
channel = connection.channel()

channel.queue_declare(queue='server1', durable=True)

# n RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange.
with open('test.yaml','r') as f:
    data = f.read()
channel.basic_publish(exchange='',
                      routing_key='server',
                      body=data,
                      properties=pika.BasicProperties(delivery_mode=2)   # 设置消息持久化，将要发送的消息的属性标记为2，表示该消息要持久化)
                      )
print('----end----')
channel.close()
connection.close()
