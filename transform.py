import pandas as pd
from pymongo import MongoClient

def get_raw_data():
   client = MongoClient('localhost', 27017)
   db = client['texas_health']
   collection = db['tx_covid']
   data = list(collection.find())
   df = pd.DataFrame(data)
   return df

def clean_data(df):
   df = df.drop(columns=['_id', 'group', 'data_as_of', 'year', 'state', 'flag', 'month'])
   df = df[df.age_group != 'Not stated']
   df['covid_19_deaths'] = pd.to_numeric(df['covid_19_deaths'])
   df['number_of_mentions'] = pd.to_numeric(df['number_of_mentions'])
   df = df.dropna(subset=['covid_19_deaths', 'number_of_mentions'])
   df['start_date'] = pd.to_datetime(df['start_date'])
   df['end_date'] = pd.to_datetime(df['end_date'])
   return df

if __name__ == '__main__':
   df = get_raw_data()
   df = clean_data(df)
   print(df.head())
   print(df.info())
   
   