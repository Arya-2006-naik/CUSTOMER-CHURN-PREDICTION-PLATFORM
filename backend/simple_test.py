from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Simple test backend working"}

@app.get("/metrics")
def get_metrics():
    return {"total_customers": 8432, "churn_rate": 23.5, "high_risk_customers": 127}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
