import pandas as pd 
import psycopg2
from transform import get_raw_data, clean_data

def load_data():
   covid_data = get_raw_data()
   covid_data = clean_data(covid_data)
   
   conn = psycopg2.connect(dbname='tx_covid_2021', user='naga', host='localhost')
   cur = conn.cursor()
   
   cur.execute('DROP TABLE IF EXISTS covid_data CASCADE;')
   
   cur.execute('''
               CREATE TABLE texas_covid (
                  start_date DATE,
                  end_date DATE,
                  condition_group TEXT,
                  condition TEXT,
                  icd10_codes TEXT,
                  age_group TEXT,
                  covid_19_deaths FLOAT,
                  number_of_mentions FLOAT)
               ''')
   
   for _, row in covid_data.iterrows():
      cur.execute(
         "INSERT INTO texas_covid VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
         tuple(row)
    )
   
   conn.commit()
   cur.close()
   conn.close()
   
if __name__ == '__main__':
   load_data()
   print('Data loaded into PostgreSQL!')
