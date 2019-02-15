#-*- coding: UTF-8 -*-
import json
import pika


credentials = pika.PlainCredentials('admin','password')
# 创建链接
connection = pika.BlockingConnection(pika.ConnectionParameters(
    'ip',5672,'/',credentials))

# 创建频道
channel = connection.channel()

# 创建模糊匹配类型的exchange
channel.exchange_declare(exchange='server',
                         exchange_type='direct')

routing_key = 'start'

with open('test.yaml','r') as f:
    data = f.read()
    data = json.dumps(data, indent=2, ensure_ascii=False)
channel.basic_publish(exchange='server',
                      routing_key=routing_key,
                      body=data)
print('---')
channel.close()
connection.close()
