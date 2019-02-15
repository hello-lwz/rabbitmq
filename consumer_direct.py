# _*_coding:utf-8_*_
import json
import pika


credentials = pika.PlainCredentials('admin','password')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    'ip',5672,'/',credentials))
channel = connection.channel()


channel.exchange_declare(exchange='server',
                         exchange_type='direct')  # 声明exchange的类型为模糊匹配。

result = channel.queue_declare(exclusive=True)  # 创建随机一个队列当消费者退出的时候，该队列被删除
queue_name = result.method.queue  # 创建一个随机队列名字。

binding_keys = ['start']

for binding_key in binding_keys:
    channel.queue_bind(exchange='server',
                       queue=queue_name,
                       routing_key=binding_key)

def callback(ch, method, properties, body):
    with open('consumer.yaml','w') as f:
        print('------------')
        body = body.decode()
        data = json.loads(body)
        f.write(data)
        # print('start')

channel.basic_consume(callback,
                      queue=queue_name
                      )
channel.start_consuming()
