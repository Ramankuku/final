from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

# Define input data model
class CustomerData(BaseModel):
    Income: float
    CCAvg: float
    Education: int
    Mortgage: float
    CD_Account: int

app = FastAPI()

# Allow CORS for all origins (for local testing with Streamlit frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model at startup
with open("src/Notebook/tree_model.pkl", "rb") as f:
    model = pickle.load(f)

from fastapi.responses import JSONResponse, HTMLResponse

@app.get("/", response_class=HTMLResponse)
def root():
    html_content = """
    <html>
        <head>
            <title>Backend API</title>
        </head>
        <body>
            <h1>Backend API is running</h1>
            <p>Use POST /predict to get predictions.</p>
            <p>You can also use GET /predict with query parameters:</p>
            <ul>
                <li>Income (float)</li>
                <li>CCAvg (float)</li>
                <li>Education (int)</li>
                <li>Mortgage (float)</li>
                <li>CD_Account (int)</li>
            </ul>
            <p>Example GET request:</p>
            <code>/predict?Income=50000&CCAvg=5.5&Education=2&Mortgage=10000&CD_Account=1</code>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/favicon.ico")
def favicon():
    return JSONResponse(content={"message": "No favicon available."})

from fastapi import Query

@app.get("/predict")
def predict_get(
    Income: float = Query(...),
    CCAvg: float = Query(...),
    Education: int = Query(...),
    Mortgage: float = Query(...),
    CD_Account: int = Query(...)
):
    data = CustomerData(
        Income=Income,
        CCAvg=CCAvg,
        Education=Education,
        Mortgage=Mortgage,
        CD_Account=CD_Account
    )
    print(f"Received data for prediction (GET): {data}")
    input_data = np.array([[data.Income, data.CCAvg, data.Education, data.Mortgage, data.CD_Account]])
    prediction = model.predict(input_data)[0]
    result = "pass" if prediction == 1 else "fail"
    print(f"Prediction result (GET): {result}")
    return {"prediction": result}

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import status
from fastapi.exception_handlers import request_validation_exception_handler

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"Validation error for request {request.url}: {exc}")
    return await request_validation_exception_handler(request, exc)

@app.post("/predict")
async def predict_post(data: CustomerData):
    try:
        print(f"Received data for prediction (POST): {data}")
        input_data = np.array([[data.Income, data.CCAvg, data.Education, data.Mortgage, data.CD_Account]])
        prediction = model.predict(input_data)[0]
        result = "pass" if prediction == 1 else "fail"
        print(f"Prediction result (POST): {result}")
        return {"prediction": result}
    except Exception as e:
        print(f"Error during prediction: {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": str(e)})
