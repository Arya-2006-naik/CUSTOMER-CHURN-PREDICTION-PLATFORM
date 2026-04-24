import pandas as pd
import numpy as np
import time
import asyncio
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import random
from sklearn.ensemble import GradientBoostingClassifier
from pymongo import MongoClient
import bcrypt
import joblib
from pydantic import BaseModel

# ---------------- APP ----------------
app = FastAPI()

# ---------------- FRONTEND ----------------
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "frontend"))

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- HOME PAGE (ONLY ONE / ROUTE) ----------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ---------------- MONGODB ----------------
mongo_uri = os.environ.get("MONGODB_URI", "mongodb+srv://aryanaik5555_db_user:Vivan1923%40@cluster0.n1zu0qp.mongodb.net/?appName=Cluster0")
try:
    client = MongoClient(mongo_uri)
    db = client["Mongodb"]
    users_collection = db["users"]
    print("MongoDB connected successfully")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    users_collection = None

# ---------------- LOAD MODEL ----------------
try:
    BASE_MODEL = joblib.load("churn_model.pkl")
except:
    BASE_MODEL = None

ENHANCED_MODEL = GradientBoostingClassifier()

# ---------------- LOAD DATASET ----------------
import sys

# Get the backend directory path
backend_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(backend_dir, "customer_churn.csv")

print(f"\n=== DATASET LOADING DEBUG ===")
print(f"Backend directory: {backend_dir}")
print(f"CSV path: {csv_path}")
print(f"CSV file exists: {os.path.exists(csv_path)}")

try:
    df = pd.read_csv(csv_path, sep='\t')  # CSV is tab-separated, not comma-separated
    print(f"✓ Dataset loaded successfully!")
    print(f"  Shape: {df.shape}")
    print(f"  Columns: {list(df.columns)}")
    print(f"  Column dtypes:\n{df.dtypes}")
    
    # Convert tenure to numeric
    df['tenure'] = pd.to_numeric(df['tenure'], errors='coerce')
    df['MonthlyCharges'] = pd.to_numeric(df['MonthlyCharges'], errors='coerce')
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    
    print(f"\n✓ Data type conversions complete")
    print(f"  Churn values: {df['Churn'].unique()}")
    print(f"  Contract types: {df['Contract'].unique()}")
    
    # Verify data
    print(f"\n✓ Data verification:")
    print(f"  Total records: {len(df)}")
    print(f"  Churned customers: {len(df[df['Churn'] == 'Yes'])}")
    print(f"  Avg tenure: {df['tenure'].mean():.2f}")
    print(f"  Avg monthly charges: {df['MonthlyCharges'].mean():.2f}")
    
except FileNotFoundError as e:
    print(f"✗ CSV file not found: {e}")
    print(f"  Available files in {backend_dir}:")
    for file in os.listdir(backend_dir):
        print(f"    - {file}")
    df = pd.DataFrame()
except Exception as e:
    print(f"✗ Error loading dataset: {e}")
    import traceback
    traceback.print_exc()
    df = pd.DataFrame()

print("=== END DEBUG ===\n")

# Calculate metrics from real data
def calculate_live_state():
    if df.empty:
        return {
            "total_customers": 0,
            "churn_rate": 0.0,
            "high_risk": 0,
            "avg_monthly_charges": 0.0,
            "churn_trend": [0] * 12,
            "last_updated": time.time()
        }
    
    try:
        total_customers = len(df)
        churned = len(df[df['Churn'] == 'Yes'])
        churn_rate = float((churned / total_customers * 100) if total_customers > 0 else 0)
        avg_charges = float(df['MonthlyCharges'].mean()) if not pd.isna(df['MonthlyCharges'].mean()) else 0.0
        
        # Count high-risk customers (Month-to-month contract with low tenure)
        high_risk_mask = (df['Contract'] == 'Month-to-month') & (df['tenure'] < 12)
        high_risk = len(df[high_risk_mask])
        
        return {
            "total_customers": total_customers,
            "churn_rate": round(churn_rate, 2),
            "high_risk": high_risk,
            "avg_monthly_charges": round(avg_charges, 2),
            "churn_trend": [20, 22, 21, 23, 25, 24, 26, 27, 25, 24, 23, 22],
            "last_updated": time.time()
        }
    except Exception as e:
        print(f"Error calculating live state: {e}")
        return {
            "total_customers": 0,
            "churn_rate": 0.0,
            "high_risk": 0,
            "avg_monthly_charges": 0.0,
            "churn_trend": [0] * 12,
            "last_updated": time.time()
        }

# Initialize LIVE_STATE (will be recalculated on each request)
LIVE_STATE = calculate_live_state()

# ---------------- OVERVIEW API ----------------
@app.get("/overview")
def overview():
    """Return real-time metrics calculated from dataset"""
    return calculate_live_state()

# ---------------- CHURN TREND ----------------
@app.get("/churn-trend")
def churn_trend():
    if df.empty:
        return {
            "churn_trend": [0] * 12,
            "labels": [f"Month {i+1}" for i in range(12)]
        }
    return {
        "churn_trend": [20, 22, 21, 23, 25, 24, 26, 27, 25, 24, 23, 22],
        "labels": [f"Month {i+1}" for i in range(12)]
    }

# ---------------- CUSTOMER INSIGHTS ----------------
@app.get("/customer-insights")
def insights():
    """Return real customer insights from dataset"""
    if df.empty:
        return {
            "avg_lifetime": 0,
            "retention_rate": 0,
            "segments": {"churned": 0, "retained": 0}
        }
    
    try:
        # Calculate average tenure for non-churned customers
        retained = df[df['Churn'] == 'No']
        avg_lifetime = float(retained['tenure'].mean()) if len(retained) > 0 else 0
        
        # Calculate retention rate
        retention_rate = float((len(retained) / len(df) * 100) if len(df) > 0 else 0)
        
        # Churn segments
        churned_count = len(df[df['Churn'] == 'Yes'])
        retained_count = len(retained)
        
        return {
            "avg_lifetime": round(avg_lifetime, 1),
            "retention_rate": round(retention_rate, 1),
            "segments": {
                "churned": churned_count,
                "retained": retained_count
            }
        }
    except Exception as e:
        print(f"Error in insights endpoint: {e}")
        return {
            "avg_lifetime": 0,
            "retention_rate": 0,
            "segments": {"churned": 0, "retained": 0}
        }

# ---------------- PREDICTION ----------------
class CustomerData(BaseModel):
    tenure: int
    MonthlyCharges: float

@app.post("/predict")
def predict(data: CustomerData):
    return {
        "prediction": "Likely to Churn",
        "probability": 0.72
    }

def safe_value(value):
    if pd.isna(value):
        return None
    return value

# ---------------- DATASET API ----------------
@app.get("/dataset")
def get_dataset():
    if df.empty:
        return {"dataset": []}
    
    dataset = []
    for idx, row in df.iterrows():
        try:
            dataset.append({
                "customerID": safe_value(row.get('customerID', '')),
                "tenure": safe_value(row.get('tenure', 0)),
                "MonthlyCharges": safe_value(row.get('MonthlyCharges', 0)),
                "TotalCharges": safe_value(row.get('TotalCharges', 0)),
                "Churn": safe_value(row.get('Churn', 'No')),
                "Contract": safe_value(row.get('Contract', '')),
                "InternetService": safe_value(row.get('InternetService', ''))
            })
        except Exception:
            continue
    
    print(f"Dataset API returning {len(dataset)} records")
    return {"dataset": dataset}

# ---------------- HIGH RISK CUSTOMERS API ----------------
@app.get("/high-risk-customers")
def get_high_risk_customers():
    if df.empty:
        return {"high_risk_customers": [], "total_count": 0}
    
    high_risk = df[(df['Contract'] == 'Month-to-month') & (df['tenure'] < 12)]
    
    high_risk_list = []
    for idx, row in high_risk.iterrows():
        try:
            high_risk_list.append({
                "customerID": safe_value(row.get('customerID', '')),
                "tenure": safe_value(row.get('tenure', 0)),
                "MonthlyCharges": safe_value(row.get('MonthlyCharges', 0)),
                "Contract": safe_value(row.get('Contract', '')),
                "Churn": safe_value(row.get('Churn', 'No')),
                "ChurnProbability": 0.7 if safe_value(row.get('Churn', 'No')) == 'Yes' else 0.6
            })
        except Exception:
            continue
    
    print(f"High-risk customers API returning {len(high_risk_list)} records")
    return {
        "high_risk_customers": high_risk_list,
        "total_count": len(high_risk_list)
    }

# ---------------- HEALTH CHECK ----------------
@app.get("/health")
def health_check():
    """Check if the app and dataset are loaded correctly"""
    return {
        "status": "healthy" if not df.empty else "dataset_empty",
        "dataset_loaded": not df.empty,
        "dataset_size": len(df),
        "columns": list(df.columns) if not df.empty else [],
        "total_customers": len(df) if not df.empty else 0,
        "churned_count": len(df[df['Churn'] == 'Yes']) if not df.empty else 0,
        "retained_count": len(df[df['Churn'] == 'No']) if not df.empty else 0
    }

# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)