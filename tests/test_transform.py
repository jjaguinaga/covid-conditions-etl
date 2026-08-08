import pandas as pd
from src.transform import DataTransformer
import pytest

def test_parse_datetime():
   transformer = DataTransformer()
   
   result = transformer._parse_datetime('01/01/2021')
   
   assert result == pd.Timestamp('2021-01-01')
   
def test_parse_numeric():
   transformer = DataTransformer()
   
   result = transformer._parse_numeric('3')
   
   assert result == 3
   
def test_transform_data_filter_ages():
   raw = pd.DataFrame({
      'start_date': ['01/01/2021', '2021-01-01', '2021-01-01'],
      'end_date': ['12/31/2021', '2021-31-12', '2021-12-31'],
      'condition_group': ['Sepsis', 'Sepsis', 'Sepsis'],
      'condition': ['Sepsis', 'Sepsis', 'Sepsis'],
      'icd10_codes': ['I46', 'I46', 'I46'],
      'age_group': ['0-24', '0-24', 'All Ages'],
      'covid_19_deaths': ['10', None, 10],
      'number_of_mentions': ['10', '10', 10]
   })
   
   transformer = DataTransformer()
   
   clean = transformer.transform_data(raw)
   
   assert len(transformer.quarantine_dfs) == 1
   assert len(transformer.quarantine_dfs[0]) == 1
   assert len(clean) == 1
   assert 'All Ages' not in clean['age_group'].values
   assert clean['start_date'].iloc[0] == pd.Timestamp('2021-01-01')
   assert clean['end_date'].iloc[0] == pd.Timestamp('2021-12-31')
   assert clean['number_of_mentions'].iloc[0] == 10
   assert clean['covid_19_deaths'].iloc[0] == 10
   