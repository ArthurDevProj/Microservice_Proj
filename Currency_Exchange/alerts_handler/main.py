from kafka import KafkaConsumer
bootstrap_servers = ['localhost:9092']
topicName = 'myTopic'
consumer = KafkaConsumer(
    topicName,
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True)

for message in consumer:
    print(message)



