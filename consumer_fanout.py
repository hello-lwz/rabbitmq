# _*_coding:utf-8_*_
import json
import sys

import pika

credentials = pika.PlainCredentials('admin','password')  # 账户 密码
connection = pika.BlockingConnection(pika.ConnectionParameters(
    'ip',5672,'/',credentials))  # ip 端口
channel = connection.channel()


channel.exchange_declare(exchange='server2',     # 交换机名字
                         exchange_type='fanout')  # 声明exchange的类型为广播模式。

result = channel.queue_declare(exclusive=True)  # 创建随机一个队列当消费者退出的时候，该队列被删除
queue_name = result.method.queue  # 创建一个随机队列名字。

channel.queue_bind(exchange='server2',
                   queue=queue_name
                   )

def callback(ch, method, properties, body):
    with open('consumer.yaml','w') as f:
        print('------------')
        body = body.decode()
        data = json.loads(body)
        # f.write(data)
        print(data)

channel.basic_consume(callback,
                      queue=queue_name
                      )
channel.start_consuming() # 等待接受消息
