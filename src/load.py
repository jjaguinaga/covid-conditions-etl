import pandas as pd
import psycopg2
from io import StringIO
from config.settings import settings
from src.logger import get_logger

class DataLoader:
   
   def __init__(self):
      self.logger = get_logger('load')
      
      self.conn = None
      
      self.cur = None
      
   def __enter__(self):
      self.conn = psycopg2.connect(settings.database_url)
      
      self.cur = self.conn.cursor()
      
      return self
   
   def __exit__(self, exc_type, exc_value, traceback):
      if exc_type is not None:
         self.conn.rollback()
         
         self.logger.error(f'Error occurred: {exc_value}')
         
      else:
         self.conn.commit()
         
         self.logger.info('committed successfully')
         
      self.cur.close()
      
      self.conn.close()
      
   def _create_staging_table(self, table_name, schema_sql):
      staging_name = f'{table_name}_staging'
      
      self.cur.execute(f'DROP TABLE IF EXISTS {staging_name} CASCADE;')
      
      self.cur.execute(f'CREATE TABLE {staging_name} ({schema_sql});')
      
      self.logger.info(f'Staging table {staging_name} created')
      
      return staging_name
   
   def _bulk_insert(self, df, table_name):
      buffer = StringIO()
      
      df.to_csv(buffer, index=False, header=False)
      
      buffer.seek(0)
      
      self.cur.copy_from(buffer, table_name, sep=',', columns=df.columns.tolist())
      
      self.logger.info(f'Loaded {table_name}')
      
   def _swap_tables(self, staging_name, final_name):
      backup = f'{final_name}_old'
      
      self.cur.execute('''
                       SELECT EXISTS (
                          SELECT FROM information_schema.tables
                          WHERE table_name = %s);''',
                        (final_name,)
      )
      
      exists = self.cur.fetchone()[0]
      
      if exists:
         self.cur.execute(f'DROP TABLE IF EXISTS {backup};')
         
         self.cur.execute(f'ALTER TABLE {final_name} RENAME TO {backup};')
         
      self.cur.execute(f'ALTER TABLE {staging_name} RENAME TO {final_name};')
      
      if exists:
         self.cur.execute(f'DROP TABLE {backup};')
      
      self.logger.info(f'Swapped {staging_name} to {final_name}')
         
   def load_table(self, df):
      schema = '''
         start_date DATE,
         end_date DATE,
         condition_group TEXT,
         condition TEXT,
         icd10_codes TEXT,
         age_group TEXT,
         covid_19_deaths INTEGER,
         number_of_mentions INTEGER'''
         
      staging = self._create_staging_table('covid_table', schema)
      
      self._bulk_insert(df, staging)
      
      self._swap_tables(staging, 'covid_table')
      
   def run_full_load(self, df):
      self.logger.info('Starting full database load...')
      
      self.load_table(df)
      
      self.logger.info('Full load complete!')
      