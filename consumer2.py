# _*_coding:utf-8_*_
import pika


credentials = pika.PlainCredentials('admin','password')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    'ip',5672,'/',credentials))
channel = connection.channel()

# 设置队列名字 和持久化
channel.queue_declare(queue='server1', durable=True)

def callback(ch, method, properties, body):
    with open('consumer.yaml','w') as f:

        body = body.decode()
        f.write(body)
        # print(body)
        print('----succeed2-----')
        ch.basic_ack(delivery_tag=method.delivery_tag)  # 接收到消息后会给rabbitmq发送一个确认

channel.basic_qos(prefetch_count=1)   # 消费者给rabbitmq发送一个信息：在消费者处理完消息之前不要再给消费者发送消息

channel.basic_consume(callback,
                      queue='server'
                      )
channel.start_consuming()
