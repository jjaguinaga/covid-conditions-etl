import pandas as pd
from config.settings import settings
from src.logger import get_logger
from datetime import datetime

class DataTransformer:
   
   def __init__(self):
      self.logger = get_logger('transform')
      
      self.quarantine_dfs = []
      
      self._clear_quarantine()
      
   def _clear_quarantine(self):
      for file in settings.QUARANTINE_DATA_PATH.glob('quarantine_*.csv'):
         file.unlink()
         
      self.logger.info('Cleared old quarantine files')
         
   def _save_quarantine(self, df, name):
      timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
      
      if df.empty:
         return 
      
      filename = settings.QUARANTINE_DATA_PATH / f'quarantine_{name}_{timestamp}.csv'
      
      df.to_csv(filename, index=False)
      
      self.logger.info(f'Quarantined {len(df)} rows to {filename}')
      
      self.quarantine_dfs.append(df)
      
   def _parse_datetime(self, column):
      return pd.to_datetime(column, format='mixed', errors='coerce')
   
   def _parse_numeric(self, column):
      return pd.to_numeric(column, errors='coerce')

   def transform_data(self, df):
      self.logger.info('Transforming data...')
      
      df = df[df.age_group != 'All Ages']
      
      df = df.drop(columns=['_id', 'group', 'data_as_of', 'year', 'state', 'flag', 'month'], errors='ignore')
       
      bad_agegroup = df['age_group'] == 'Not stated'
      
      if bad_agegroup.any():
         self._save_quarantine(df[bad_agegroup], 'age_group_not_stated')
         
      df = df[~bad_agegroup].copy()
      
      df['covid_19_deaths'] = df['covid_19_deaths'].apply(self._parse_numeric)

      bad_deaths = df['covid_19_deaths'].isna()
      
      if bad_deaths.any():
         self._save_quarantine(df[bad_deaths], 'covid_deaths_null')
         
      df = df[~bad_deaths].copy()
         
      df['covid_19_deaths'] = df['covid_19_deaths'].astype(int)
      
      df['number_of_mentions'] = df['number_of_mentions'].apply(self._parse_numeric)
      
      bad_mentions = df['number_of_mentions'].isna()
      
      if bad_mentions.any():
         self._save_quarantine(df[bad_mentions], 'mentions_null')
         
      df = df[~bad_mentions].copy()
      
      df['start_date'] = df['start_date'].apply(self._parse_datetime)
      
      df['end_date'] = df['end_date'].apply(self._parse_datetime)
      
      return df
   