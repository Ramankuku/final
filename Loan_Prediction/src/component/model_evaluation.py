import os
import sys
from src.logger import logging
from src.exception import MyException
from src.entity.artifact_entity import DataTransformationArtifact, ModelEvaluationArtifact
import pandas as pd 
import tempfile
import numpy as np
from src.utils.utils import load_numpy
import pickle
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, recall_score, precision_score, confusion_matrix, classification_report
import mlflow
# from utils.utils import load_numpy

class DataEvaluation:
    def __init__(self, data_transformation_artifact: DataTransformationArtifact):
        try:
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise MyException(e, sys)

    def model_train(self)->ModelEvaluationArtifact:
        try:
            logging.info('Model Training')
            train_arr = load_numpy(self.data_transformation_artifact.transformed_train_file)
            test_arr = load_numpy(self.data_transformation_artifact.transformed_test_file)
            logging.info(f'Train arr: {train_arr} ----------- Test arr: {test_arr}')

            X_train, y_train = train_arr[:, :-1], train_arr[:,-1]
            X_test, y_test = test_arr[:, :-1], test_arr[:, -1]

            print(f'X_train: {X_train.shape}\n X_test: {X_test.shape}')   
            logging.info('X_train and X_test Done shape Done!')

            #Defining the best parameters for my model
            criterion = 'entropy'
            max_depth = 4
            splitter = 'best'
            min_samples_split = 2
            min_samples_leaf =4

            logging.info('Model Building start')
            tree_model = DecisionTreeClassifier(
                criterion=criterion,
                max_depth=max_depth,
                splitter=splitter,
                min_samples_split=min_samples_split,
                min_samples_leaf=min_samples_leaf
                )
            
            tree_model.fit(X_train, y_train)
            y_pred = tree_model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            logging.info(f'Accuracy is:---------> {accuracy}')
            cm = confusion_matrix(y_test, y_pred)
            logging.info(f'Showing the confusion matrix: {cm}')
            report = classification_report(y_test, y_pred)
            logging.info(f'Classification report: {report}')

            #Dump the model
            with open('Decision_Tree_Model.pkl', 'wb') as f:
                pickle.dump(tree_model, f)

            mlflow.set_experiment('Tree Model')
            with mlflow.start_run() as run:
                mlflow.log_param('Criterion', criterion)
                mlflow.log_param('max_depth', max_depth)
                mlflow.log_param('splitter', splitter)
                mlflow.log_param('min_samples_split', min_samples_split)
                mlflow.log_param('min_samples_leaf', min_samples_leaf)

                mlflow_id = run.info.run_id
                logging.info('Model Training Completed')
            

            model_evaluate_artifact = ModelEvaluationArtifact(
                accuracy=accuracy,
                classification_report=report,
                mlflow_id=mlflow_id
            )
            logging.info(f'Model Evaluation Artifact: {model_evaluate_artifact}')
            return model_evaluate_artifact
        
        except Exception as e:
            raise MyException(e, sys)
        
    
