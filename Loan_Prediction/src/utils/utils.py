import os
import sys
import yaml
import dill 
import numpy as np
from src.logger import logging
from src.exception import MyException

def read_yaml_file(file_path: str)->dict:
    try:
        with open(file_path, 'rb') as yaml_file:
            data = yaml.safe_load(yaml_file)
            return data
    
    except Exception as e:
        raise MyException(e, sys)


def save_object(file_path: str, obj:object)->None:
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            dill.dump(obj, file_obj)

    except Exception as e:
        raise MyException(e, sys)
    


def save_numpy(file_path: str, array:np.array):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    
    except Exception as e:
        raise MyException(e, sys)
    
def load_numpy(file_path: str) -> np.ndarray:
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj, allow_pickle=True)  
    except Exception as e:
        raise MyException(e, sys)

