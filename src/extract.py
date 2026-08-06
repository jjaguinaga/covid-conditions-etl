import pandas as pd
from pathlib import Path
import json
import requests
from config.settings import settings
from src.logger import get_logger

class DataExtractor:
   
   def __init__(self, raw_path=None):
      self.raw_path = raw_path or settings.RAW_DATA_PATH
      
      self.logger = get_logger('extract')
      
   def _pull_api(self, filename: str):  
      self.logger.info(f'Getting API {filename}')
      
      url = "https://data.cdc.gov/resource/hk9y-quqm.json?$where=state='Texas' AND year=2021&$limit=3000"
      
      headers = {'Accept': 'application/json'}
      
      response = requests.get(url, timeout=30, headers=headers)
      
      response.raise_for_status()
      
      api_data = response.json()
         
      with open(self.raw_path/filename, 'w') as f:
         json.dump(api_data, f, indent=2, ensure_ascii=False)
         
      self.logger.info(f'Raw JSON saved to {filename}')
      
      df = pd.DataFrame(api_data)
      
      return df
   
   def extract_covid_data(self):
      return self._pull_api('covid_raw.json')
