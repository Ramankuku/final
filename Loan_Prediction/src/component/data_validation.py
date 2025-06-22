from src.logger import logging
from src.exception import MyException
import sys
import os
from src.entity.config_entity import DataIngestionConfig, DataValidationConfig
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from src.utils.utils import read_yaml_file
from src.constants import SCHEMA_PATH
import pandas as pd
import json
from pandas import DataFrame

class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config:DataValidationConfig):
        self.data_ingestion_artifact=data_ingestion_artifact
        self.data_validation_config = data_validation_config
        self.schema_file = read_yaml_file(file_path=SCHEMA_PATH)
    

    def is_validate(self, dataframe:DataFrame)->bool:
        try:
            status = len(dataframe.columns) == len(self.schema_file['columns'])
            logging.info(f'Validation Done: {status}')
            return status

        except Exception as e:
            raise MyException(e, sys)
    

    def is_column_exits(self, df:DataFrame)->bool:
        try:
            df_columns = df.columns
            missing_categorical_columns = []
            missing_numerical_columns = []


            #Categorical Columns
            for cate_columns in self.schema_file['categorical_columns']:
                if cate_columns not in df_columns:
                    missing_categorical_columns.append(cate_columns)
            
            if len(missing_categorical_columns)>0:
                logging.info(f'Missing Categorical columns: {missing_categorical_columns}')
            

            #Numerical Columns
            for num_cols in self.schema_file['numerical_columns']:
                if num_cols not in df_columns:
                    missing_numerical_columns.append(num_cols)
            
            if len(missing_numerical_columns)>0:
                logging.info(f'Missing Numerical columns: {missing_numerical_columns}')

            return False if len(missing_numerical_columns)>0 or len(missing_categorical_columns)>0 else True

        except Exception as e:
            raise MyException(e, sys)
    
    @staticmethod
    def read_file(file_path)->DataFrame:
        try:
            df = pd.read_csv(file_path)
            return df

        except Exception as e:
            raise MyException(e, sys)
        
    
    def initiate_validation(self)->DataValidationArtifact:
        try:
            logging.info('Validation Started')

            validation_mess = ''
            train_df, test_df = (DataValidation.read_file(file_path=self.data_ingestion_artifact.train_file_path),
        DataValidation.read_file(file_path=self.data_ingestion_artifact.test_file_path))
            logging.info("Read Train and Test")

            #Validation train Data
            status = self.is_validate(dataframe=train_df)
            if not status:
                validation_mess += 'Some columns are missing in Train data'
            else:
                logging.info(f'Status is: {status}')
            
            #Validation Test Data
            status = self.is_validate(dataframe=test_df)
            if not status:
                validation_mess +='Some columns are missing in Test Data'
            else:
                logging.info(f'Status is: {status}')

            
            validation_status = len(validation_mess)==0

            data_validation_artifact= DataValidationArtifact(
                validation_status=validation_status,
                validation_message=validation_mess,
                validated_file_path=self.data_validation_config.data_validation_file

            )


            dir_path = self.data_validation_config.data_validation_dir
            os.makedirs(dir_path, exist_ok=True)

            validation_report = {
                'validation_status': validation_status,
                'message': validation_mess.strip()
            }

            with open(self.data_validation_config.data_validation_file, 'w') as file:
                json.dump(validation_report, file, indent=4)

            logging.info(f'Saved validation report: {validation_report}')

            return data_validation_artifact



        except Exception as e:
            raise MyException(e, sys)