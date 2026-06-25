import pandas as pd
from pymongo import MongoClient
from google.cloud import bigquery
from transform import get_raw_data, clean_data

def load_to_bigquery():
   client = bigquery.Client(project="covid-bigquery-500401")
   table_id = "covid-bigquery-500401.texas_covid_2021.conditions"
   covid_data = get_raw_data()
   covid_data = clean_data(covid_data)
   job = client.load_table_from_dataframe(covid_data, table_id)
   job.result()
   print('Data ready!!')
   
if __name__ == '__main__':
   load_to_bigquery()
   print('Data loaded!!')