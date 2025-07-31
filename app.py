"""uvicorn app:app --reload"""
from fastapi import FastAPI

import pickle
import pandas as pd
from fastapi.responses import JSONResponse
from schema.user import UserInput
from schema.prediction_response import PredictionResponse
from model.predict import predict_output, model, MODEL_VERSION


app = FastAPI()

@app.get('/')
def home():
    return JSONResponse(status_code=200, content={'message': 'Welcome to the Health Insurance Premium Prediction API'})

@app.get('/health')
def health_check():
    return JSONResponse(status_code=200, content={'status': 'healthy', 'version': MODEL_VERSION, 'model': 'Health Insurance Premium Predictor  Model'})

@app.post('/predict', response_model=PredictionResponse)
def predict_premium(data: UserInput):
    user_input = {
        'bmi': data.bmi,
        'lifestyle_risk': data.lifestyle_risk,
        'age_group': data.age_group,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }
    try:
        prediction = predict_output(user_input)
    except Exception as e:
        return JSONResponse(status_code=500, content={'error': str(e)})
    return JSONResponse(status_code=200, content={'predicted_category': prediction})
