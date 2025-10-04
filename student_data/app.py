from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

model = joblib.load("model.joblib") 

app = FastAPI()
class FaceFeatures(BaseModel):
    IQ: int
    CGPA: float
    Academic_Performance: int
    Communication_Skills: int
    Projects_Completed: int

@app.post("/predict/")
def predict_gender(features: FaceFeatures):
    
    input_data = np.array([[ 
        features.IQ,
        features.CGPA,
        features.Academic_Performance,
        features.Communication_Skills,
        features.Projects_Completed,
        
    ]])
    
    prediction = model.predict(input_data)
    predicted_class = int(prediction[0])  
    return {"prediction": predicted_class}
