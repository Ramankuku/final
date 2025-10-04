import os
import sys
from src.logger import logging
from src.exception import MyException
import numpy as np 
import pandas as pd
from pandas import DataFrame
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder
from src.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig
from src.constants import *
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact
from src.constants import SCHEMA_PATH, TARGET
from src.utils.utils import read_yaml_file, save_numpy, save_object
from sklearn.pipeline import Pipeline



class DataTransformation:
    def __init__(self, data_ingestion_artifact:DataIngestionArtifact, data_validation_artifact: DataValidationArtifact, data_transformation_config: DataTransformationConfig):

        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config   
            self.schema_file = read_yaml_file(file_path=SCHEMA_PATH)

        except Exception as e:
            raise MyException(e, sys)
        
    def read_csv_file(self, file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        
        except Exception as e:
            raise MyException(e, sys)
    
    def transformation(self)->Pipeline:
        try:
            categorical_encoder = self.schema_file['categorical_ordinal_encoder_columns']

            processor = ColumnTransformer(transformers=[
                ('ordinal', OrdinalEncoder(), categorical_encoder)
            ], remainder='passthrough')

            pipeline = Pipeline(steps=[('processor', processor)])
            return pipeline

        except Exception as e:
            raise MyException(e, sys)
    
    def drop_columns(self, df):
        try:
            logging.info('Dropping columns')
            drop_columns = self.schema_file['drop_columns']
            df = df.drop(columns=[col for col in drop_columns if col in df.columns], axis=1)
            logging.info(f'After droping columns from Dataframe: ------------> {df}')
            return df
        
        except Exception as e:
            raise MyException(e, sys)
    
    def convert_ccavg(self, df):
        try:
            logging.info('Converting of CCAVG')
            convert_ccavg = self.schema_file['ccavg_convert']
            for i in convert_ccavg:
                if i in df.columns:
                    df[i] = df[i].astype(str).str.replace('/', '.')
                    df[i] = df[i].astype(float)*12
            
            return df
        
        except Exception as e:
            raise MyException(e, sys)
    
   
    
    def columns_conversion(self, df):
        try:
            logging.info('Label Columns Converting')
            columns = self.schema_file['conversion_columns']
            for col in columns:
                if col in df.columns:
                    df[col] = df[col].apply(lambda x: 1 if str(x).strip().lower() == 'yes' else 0)
            
            return df
        


        except Exception as e:
            raise MyException(e, sys)
   
    
    def initiate_transformation(self)->DataTransformationArtifact:
        try:
            train_df = self.read_csv_file(file_path=self.data_ingestion_artifact.train_file_path)
            test_df = self.read_csv_file(file_path=self.data_ingestion_artifact.test_file_path)
            logging.info('Train and test separated')
            
            train_df[TARGET] = train_df[TARGET].map({'Yes':1, 'No':0})
            test_df[TARGET] = test_df[TARGET].map({'Yes':1, 'No':0})


            input_train_feature = train_df.drop(columns=[TARGET], axis=1)
            target_train_feature = train_df[TARGET].values.reshape(-1, 1)

            input_test_feature = test_df.drop(columns=[TARGET], axis=1)
            target_test_feature = test_df[TARGET].values.reshape(-1, 1)
            logging.info(input_train_feature)

            #Convert CCAVG 
            input_train_feature = self.convert_ccavg(input_train_feature)
            input_test_feature = self.convert_ccavg(input_test_feature)

            #Converting columns
            input_train_feature = self.columns_conversion(input_train_feature)
            input_test_feature = self.columns_conversion(input_test_feature)

            #Dropping Columns
            input_train_feature = self.drop_columns(input_train_feature)
            input_test_feature = self.drop_columns(input_test_feature)
            logging.info(f'Input train feature: {input_train_feature.shape}')

            processor = self.transformation()

            input_train_feature_arr = processor.fit_transform(input_train_feature)
            input_test_feature_arr = processor.transform(input_test_feature)
            # logging.info(f'Train shape: {input_train_feature_arr.shape} -----> Test shape: {input_test_feature_arr}')

            train_arr = np.c_[input_train_feature_arr, np.array(target_train_feature)]
            test_arr = np.c_[input_test_feature_arr, np.array(target_test_feature)]
            logging.info(f'Train arr shape -------> {train_arr}')

            save_object(self.data_transformation_config.transformed_object_path, processor)
            save_numpy(self.data_transformation_config.transformed_train_file, array=train_arr)
            save_numpy(self.data_transformation_config.transformed_test_file, array=test_arr)


            return DataTransformationArtifact(
                transformed_object=self.data_transformation_config.transformed_object_path,
                transformed_train_file=self.data_transformation_config.transformed_train_file,
                transformed_test_file=self.data_transformation_config.transformed_test_file
            )
        
        except Exception as e:
            raise MyException(e, sys)
    

        