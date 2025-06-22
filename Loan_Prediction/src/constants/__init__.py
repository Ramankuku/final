import os

#Database Setup

DB_NAME = 'Loan-Status-pred'
CONNECTION_NAME = 'Loan-Status-pred-data'
MONGODB_URL_KEY = 'MONGODB_URL' 



PIPELINE_NAME: str = ''
ARTIFACT_DIR: str = 'artifact'
FILE_NAME: str = 'data.csv'
TRAIN_FILE_NAME: str = 'train.csv'
TEST_FILE_NAME: str = 'test.csv'
PREPROCESSED_PATH: str = 'processor.pkl'
SCHEMA_PATH: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data_cols', 'schema.yaml'))

#Constants for data ingestion File

DATA_INGESTION_COLLECTION_NAME: str = 'Loan-Status-pred-data'
DATA_INGESTION_DIR_NAME: str = 'data-ingestion'
DATA_INGESTION_FEATURE_STORE_DIR: str = 'feature-store'
DATA_INGESTION_INGESTED_DIR: str = 'ingested'
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

#Validation 
DATA_VALIDATION_DIR_NAME:str = 'validated'
DATA_VALIDATION_FILE_NAME: str = 'report.yaml'

#Transformation 

DATA_TRANSFORMED_DIR_NAME:str = 'data-transformed'
DATA_TRANSFORMED_FILE_NAME: str = 'transformed'
DATA_TRANSFORMED_OBJECT_PATH: str = 'transformed-file'




#Declaring Target Variable 
TARGET = 'Personal Loan'
