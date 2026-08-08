from src.extract import DataExtractor
from src.transform import DataTransformer
from src.load import DataLoader
from src.logger import get_logger

def main():
   logger = get_logger('pipeline')
   
   logger.info('Starting pipeline...')

   extractor = DataExtractor()
   
   covid_df = extractor.extract_covid_data()
   
   logger.info(f'COVID DataFrame extracted')
   
   transformer = DataTransformer()
   
   clean_covid = transformer.transform_data(covid_df)
   
   logger.info(f'COVID data transformed')
   
   with DataLoader() as loader:
      loader.run_full_load(clean_covid)
      
   logger.info(f'Data loaded to PostgreSQL {len(clean_covid)} rows')
   
   logger.info('Pipeline completed!')
   
if __name__ == '__main__':
   main()