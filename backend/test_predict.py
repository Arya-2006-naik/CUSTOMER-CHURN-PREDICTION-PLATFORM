from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

body = {
    'gender': 'Female',
    'SeniorCitizen': 0,
    'Partner': 'No',
    'Dependents': 'No',
    'tenure': 12,
    'PhoneService': 'Yes',
    'MultipleLines': 'No',
    'InternetService': 'DSL',
    'Contract': 'Month-to-month',
    'PaperlessBilling': 'Yes',
    'PaymentMethod': 'Electronic check',
    'MonthlyCharges': 70.35,
    'TotalCharges': 848.8
}

resp = client.post('/predict', json=body)
print('status', resp.status_code)
print('json', resp.json())
print('text', resp.text)
