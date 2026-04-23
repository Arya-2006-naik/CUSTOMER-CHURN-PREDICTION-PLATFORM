import pandas as pd
import numpy as np
from fastapi import FastAPI
import joblib
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model with absolute path
try:
    MODEL = joblib.load(r"C:\Users\Admin\Downloads\CUSTOMER CHURN PREDICTION PLATFORM\backend\churn_model.pkl")
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")
    MODEL = None

@app.get("/")
def home():
    return {"message": "Welcome to Churn Prediction API"}

@app.get("/metrics")
def get_metrics():
    try:
        df = pd.read_csv(r'C:\Users\Admin\Downloads\CUSTOMER CHURN PREDICTION PLATFORM\backend\customer_churn.csv')
        total_customers = len(df)
        churn_rate = (df['Churn'].sum() / len(df) * 100) if 'Churn' in df.columns else 23.5
        high_risk = len(df[(df['tenure'] < 12) & (df['MonthlyCharges'] > 80)])
        avg_tenure_churned = df[df['Churn'] == 1]['tenure'].mean() if 'Churn' in df.columns else 15.2
        avg_monthly_charges = df['MonthlyCharges'].mean() if 'MonthlyCharges' in df.columns else 75.5
        
        return {
            "total_customers": total_customers,
            "churn_rate": round(churn_rate, 1),
            "high_risk_customers": high_risk,
            "avg_tenure_churned": round(avg_tenure_churned, 1),
            "avg_monthly_charges": round(avg_monthly_charges, 2)
        }
    except Exception as e:
        return {"error": str(e)}

class CustomerData(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float

@app.post("/predict")
def predict(data: CustomerData):
    if MODEL is None:
        return {"error": "Model not loaded"}
    
    try:
        input_dict = data.dict()
        df = pd.DataFrame([input_dict])
        df = pd.get_dummies(df)
        
        model_columns = MODEL.feature_names_in_
        for col in model_columns:
            if col not in df:
                df[col] = 0
        df = df[model_columns]
        
        prediction = MODEL.predict(df)[0]
        probability = MODEL.predict_proba(df)[0][1]
        
        # Determine risk level
        if probability > 0.70:
            risk_level = "High"
        elif probability >= 0.40:
            risk_level = "Medium"
        else:
            risk_level = "Low"
        
        # Get reasons
        reasons = []
        if input_dict.get('MonthlyCharges', 0) > 80:
            reasons.append("High monthly charges")
        if input_dict.get('tenure', 0) < 12:
            reasons.append("Low tenure")
        if input_dict.get('Contract', '') == 'Month-to-month':
            reasons.append("Month-to-month contract")
        
        return {
            "prediction": "Likely to Churn" if prediction == 1 else "Not Likely to Churn",
            "probability": round(probability * 100, 1),
            "risk_level": risk_level,
            "reasons": reasons[:3],
            "retention_strategy": {
                "category": risk_level + " Risk",
                "actions": [
                    "Offer discount" if risk_level == "High" else "Loyalty points",
                    "Dedicated support" if risk_level == "High" else "Email campaign",
                    "Free upgrade" if risk_level == "High" else "Bundle offer"
                ]
            }
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
