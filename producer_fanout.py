#-*- coding: UTF-8 -*-
import json
import pika


credentials = pika.PlainCredentials('guest','guest') # rabbitmq user pw
# 创建链接
connection = pika.BlockingConnection(pika.ConnectionParameters(
    'ip',端口,'/',credentials))

# 创建频道
channel = connection.channel()

# 创建模糊匹配类型的exchange
channel.exchange_declare(exchange='server2',
                         exchange_type='fanout')


with open('test.yaml','r') as f:
    data = f.read()
    data = json.dumps(data, indent=2, ensure_ascii=False)
    # 从文件读出数据 转化为json  也可以不转化
channel.basic_publish(exchange='server2',
                      routing_key='',
                      body=data)
print('---')
channel.close()
connection.close()
