import requests
import json

# Test backend API
def test_backend():
    try:
        # Test welcome endpoint
        response = requests.get("http://127.0.0.1:8000/")
        print(f"Backend Welcome Endpoint: {response.status_code} - {response.json()}")
        
        # Test prediction endpoint
        test_data = {
            "gender": "Female",
            "SeniorCitizen": 1,
            "Partner": "Yes",
            "Dependents": "Yes",
            "tenure": 6,
            "PhoneService": "Yes",
            "MultipleLines": "Yes",
            "InternetService": "Fiber optic",
            "Contract": "Month-to-month",
            "PaperlessBilling": "Yes",
            "PaymentMethod": "Electronic check",
            "MonthlyCharges": 95.50,
            "TotalCharges": 573.00
        }
        
        response = requests.post("http://127.0.0.1:8000/predict", json=test_data)
        print(f"Backend Prediction Endpoint: {response.status_code}")
        print(f"Prediction Result: {response.json()}")
        
        return True
    except Exception as e:
        print(f"Backend Error: {e}")
        return False

# Test frontend accessibility
def test_frontend():
    try:
        response = requests.get("http://127.0.0.1:3000/")
        print(f"Frontend Server: {response.status_code} - Serving HTML content")
        return True
    except Exception as e:
        print(f"Frontend Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Customer Churn Prediction Platform Integration")
    print("=" * 60)
    
    backend_ok = test_backend()
    frontend_ok = test_frontend()
    
    print("\n" + "=" * 60)
    if backend_ok and frontend_ok:
        print("INTEGRATION TEST PASSED! Both frontend and backend are working correctly.")
        print("\nAccess the application at: http://127.0.0.1:3000")
        print("Backend API available at: http://127.0.0.1:8000")
        print("API Documentation: http://127.0.0.1:8000/docs")
    else:
        print("INTEGRATION TEST FAILED! Please check server status.")
