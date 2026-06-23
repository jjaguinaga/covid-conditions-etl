import requests
from pymongo import MongoClient

def extract_data():
   url = "https://data.cdc.gov/resource/hk9y-quqm.json?$where=state='Texas' AND year=2021&$limit=3000"
   headers = {'Accept': 'application/json'}
   response = requests.get(url, timeout=30, headers=headers)
   return response.json()

def store_raw_data(data):
   client = MongoClient('localhost', 27017)
   db = client['texas_health']
   collection = db['tx_covid']
   collection.delete_many({})
   collection.insert_many(data)
   print('Data loaded!')
   
   
if __name__ == '__main__':
   results = extract_data()
   store_raw_data(results)
   
