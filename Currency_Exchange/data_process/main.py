import json
import requests
import pymongo as mongodb
from pprint import pprint
import schedule
import time

API_URL = "https://api.exchangerate.host/lastest"


def get_response(URL: str):
    response = requests.get(URL)
    return response.json()


def data_processor():
    with open("../config.json", 'r') as cnf:
        cnf_j = json.load(cnf)

    currencies_names = [curr['name'] for curr in cnf_j['currencies']]
    dict_of_res = get_response(f"{API_URL}?symbols={','.join(currencies_names)}")
    clean_result = {'base': dict_of_res['base'],
                    'date': dict_of_res['date'],
                    'rates': dict_of_res['rates']
                    }
    pprint(clean_result)
    insert_to_db(clean_result)


def insert_to_db(dict_of_res: dict):
    client = mongodb.MongoClient('localhost', 27017)
    db = client['currencies']
    collection = db['rates_currencies']
    collection.insert_one(dict_of_res)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    schedule.every().day.at('00:00').do(data_processor)
    while True:
        schedule.run_pending()
        time.sleep(1)