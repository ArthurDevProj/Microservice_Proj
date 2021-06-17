import json
import requests
import pymongo as mongodb
from pprint import pprint
import schedule
import time
from kafka import KafkaProducer

API_URL = "https://api.exchangerate.host/lastest"


def get_response(URL: str):
    response = requests.get(URL)
    return response.json()


def check_in_db():
    topicName = 'myTopic'
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

    client = mongodb.MongoClient('localhost', 27017)
    db = client['currencies']
    collection = db['rates_currencies']

    with open("../config.json", 'r') as cnf:
        cnf_j = json.load(cnf)
    currencies_name_threshold = [(dict['name'], dict['threshold']) for dict in cnf_j["currencies"]]
    for name,threshold in currencies_name_threshold:
        if collection.find_one({f"rates.{name}": {"$gte": threshold}}):
            #pprint(collection.find_one({f"rates.{name}": {"$gte": threshold}}))
            ack = producer.send(topicName, b'The Alert in On')
            metadata = ack.get()
            print(metadata)

if __name__ == '__main__':
    schedule.every(5).seconds.do(check_in_db)
    while True:
        schedule.run_pending()
        time.sleep(1)