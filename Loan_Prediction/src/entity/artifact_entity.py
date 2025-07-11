from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    train_file_path: str
    test_file_path: str 


@dataclass
class DataValidationArtifact:
    validation_status: bool
    validation_message:str
    validated_file_path: str

@dataclass
class DataTransformationArtifact:
    transformed_object: str
    transformed_train_file: str
    transformed_test_file: str


@dataclass
class ModelEvaluationArtifact:
    accuracy: float
    classification_report: str
    mlflow_id: str
    