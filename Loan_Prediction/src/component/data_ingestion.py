import os 
import sys
from pandas import DataFrame
from src.constants import *
from src.logger import logging
from src.exception import MyException
from src.entity.config_entity import DataPipeLineConfig, DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from sklearn.model_selection import train_test_split 
from src.data_access.ProjectData import Proj1Data


class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig=DataIngestionConfig()):
        try:
            self.data_ingestion_config = data_ingestion_config
    
        
        except Exception as e:
            raise MyException(e, sys)
    

    def fetch_data(self)->DataFrame:
        try:
            data_base = Proj1Data()
            dataframe = data_base.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)
            logging.info(f'Dataframe shape is: {dataframe.shape}')

            feature_path = self.data_ingestion_config.data_feature_store_dir
            dir_name = os.path.dirname(feature_path)
            os.makedirs(dir_name, exist_ok=True)
            dataframe.to_csv(feature_path, index=False, header=True)
            logging.info('Converting to csv')

            return dataframe

        except Exception as e:
            raise MyException(e, sys)
    
    def split_data(self, dataframe:DataFrame)->None:
        try:
            train_data, test_data = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_ratio)
            logging.info(f'Splitting done!\n Train_data: {train_data} ----- Test_data: {test_data}')
            file_path = self.data_ingestion_config.train_file_path
            dir_names = os.path.dirname(file_path)
            os.makedirs(dir_names, exist_ok=True)

            train_data = train_data.to_csv(self.data_ingestion_config.train_file_path, index=False, header=True)
            test_data = test_data.to_csv(self.data_ingestion_config.test_file_path, index=False, header=True)
            logging.info('Train and Test data folders are made')

        except Exception as e:
            raise MyException(e, sys)
    

    def initiate_data(self)->DataIngestionArtifact:
        try:
            logging.info('Call all functions')
            dataframe=self.fetch_data()
            logging.info('Fetching Data')
            self.split_data(dataframe)
            logging.info('Splitting Done finally')

            data_artifact_ingestion = DataIngestionArtifact(train_file_path=self.data_ingestion_config.train_file_path, test_file_path=self.data_ingestion_config.test_file_path)

            return data_artifact_ingestion


        except Exception as e:
            raise MyException(e, sys)

        