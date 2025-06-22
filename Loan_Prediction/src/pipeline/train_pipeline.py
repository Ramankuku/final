from src.logger import logging
import sys
from src.exception import MyException
from src.component.data_ingestion import DataIngestion
from src.component.data_validation import DataValidation
from src.component.data_transformation import DataTransformation
from src.component.model_evaluation import DataEvaluation
from src.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelEvaluationArtifact



class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig() 


    
    def final_Ingestion_Config(self):
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data()
            logging.info('Perfomed Data Ingestion')
            return data_ingestion_artifact

        except Exception as e:
            raise MyException(e, sys)
    

    def final_validation(self, data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            data_valid = DataValidation(data_ingestion_artifact=data_ingestion_artifact, data_validation_config=self.data_validation_config)
            data_validation_artifact = data_valid.initiate_validation()
            return data_validation_artifact
        
        except Exception as e:
            raise MyException(e, sys)
    
    def final_transformation(self, data_ingestion_artifact:DataIngestionArtifact, data_validation_artifact:DataValidationArtifact)->DataTransformationArtifact:
        try:
            data_transformation = DataTransformation(data_ingestion_artifact=data_ingestion_artifact,
                                                     data_transformation_config=self.data_transformation_config,
                                                     data_validation_artifact=data_validation_artifact
            )
            data_transformation_artifact = data_transformation.initiate_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise MyException(e, sys)
    
    def final_evaluation(self, data_transformation_artifact: DataTransformationArtifact)->ModelEvaluationArtifact:
        try:
            data_transformation = DataEvaluation(data_transformation_artifact=data_transformation_artifact)
            data_evaluation_artift = data_transformation.model_train()
            return data_evaluation_artift
        
        except Exception as e:
            raise MyException(e, sys)

        



    def run_pipeline(self)->None:
        try:
            data_ingestion_artifact = self.final_Ingestion_Config()
            data_validation_artifact = self.final_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.final_transformation(data_ingestion_artifact=data_ingestion_artifact, data_validation_artifact=data_validation_artifact)
            data_evaluation_aertifact = self.final_evaluation(data_transformation_artifact=data_transformation_artifact)

        
        except Exception as e:
            raise MyException(e, sys)



    