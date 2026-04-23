import requests
import time

# Wait a moment for server to start
time.sleep(2)

try:
    response = requests.get("http://127.0.0.1:8000/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test metrics endpoint
    response = requests.get("http://127.0.0.1:8000/metrics")
    print(f"Metrics Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Metrics: {response.json()}")
    else:
        print(f"Metrics Error: {response.text}")
        
except Exception as e:
    print(f"Error: {e}")
