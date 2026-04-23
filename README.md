# Customer Churn Prediction Platform

A full-stack web application that predicts customer churn using machine learning. The platform features a modern, responsive frontend built with HTML, CSS, and JavaScript, integrated with a FastAPI backend running a trained ML model.

## Features

- **User Authentication**: Secure login system with demo account
- **Interactive Dashboard**: Real-time churn analytics and insights
- **ML-Powered Predictions**: Get instant churn risk predictions
- **Customer Insights**: Visual analytics and risk factor analysis
- **Modern UI**: Glassmorphism design with smooth animations

## Project Structure

```
CUSTOMER CHURN PREDICTION PLATFORM/
├── backend/
│   ├── main.py              # FastAPI backend server
│   ├── churn_model.pkl      # Trained ML model
│   └── test_predict.py     # Backend testing
├── frontend/
│   ├── index.html           # Main dashboard
│   ├── login.html           # Login page
│   └── insights.html        # Customer insights page
├── churn-ml-model/
│   ├── train_model.py       # Model training script
│   └── Telco-Customer-Churn.csv  # Dataset
├── start.bat               # Startup script
└── README.md               # This file
```

## Quick Start

### Option 1: Using the Startup Script (Recommended)

1. Double-click on `start.bat`
2. Wait for both servers to start
3. The application will open automatically in your browser at `http://127.0.0.1:3000`

### Option 2: Manual Startup

#### Start the Backend
```bash
cd backend
python main.py
```
The backend will start on `http://127.0.0.1:8000`

#### Start the Frontend
Open a new terminal and run:
```bash
cd frontend
python -m http.server 3000
```
The frontend will start on `http://127.0.0.1:3000`

## Access the Application

- **Frontend URL**: http://127.0.0.1:3000
- **Backend API**: http://127.0.0.1:8000
- **API Documentation**: http://127.0.0.1:8000/docs

## Login Credentials

Use the demo account to access the application:
- **Email**: admin@churnpredict.com
- **Password**: demo123

## API Endpoints

### GET `/`
Welcome message for the API

### POST `/predict`
Predict customer churn based on input data

**Request Body:**
```json
{
    "gender": "Male",
    "SeniorCitizen": 0,
    "Partner": "No",
    "Dependents": "No",
    "tenure": 12,
    "PhoneService": "Yes",
    "MultipleLines": "No",
    "InternetService": "Fiber optic",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 79.99,
    "TotalCharges": 959.88
}
```

**Response:**
```json
{
    "Churn Prediction": "Customer is likely to churn"
}
```

## Requirements

### Python Dependencies (Backend)
- FastAPI
- pandas
- scikit-learn
- joblib
- uvicorn
- pydantic

### Frontend Dependencies
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection (for CDN resources)

## Model Information

The ML model is trained on the Telco Customer Churn dataset and uses various customer features to predict churn risk:
- Customer demographics (gender, senior citizen status, partners, dependents)
- Service information (phone service, internet service, contracts)
- Billing details (payment method, monthly charges, total charges)
- Account tenure

## Features

### Dashboard
- Real-time KPI cards showing churn metrics
- Customer count and growth statistics
- High-risk customer alerts
- Interactive prediction form

### Customer Insights
- Churn trend analysis charts
- Customer segment distribution
- Key risk factors visualization
- High-risk customer table with action buttons

### Prediction System
- Real-time ML predictions
- Risk level assessment (Low/Medium/High)
- Confidence scores
- Personalized recommendations

## Troubleshooting

### Backend Issues
- Ensure all Python dependencies are installed: `pip install fastapi pandas scikit-learn joblib uvicorn pydantic`
- Check if the model file `churn_model.pkl` exists in the backend folder
- Verify port 8000 is not already in use

### Frontend Issues
- Ensure port 3000 is not already in use
- Check browser console for JavaScript errors
- Verify CDN resources (Tailwind CSS) are accessible

### Connection Issues
- Make sure both backend and frontend are running
- Check that the backend URL in `index.html` matches your backend server address
- Verify CORS is properly configured in the backend

## Development

### Adding New Features
1. Modify frontend HTML/CSS/JS files in the `frontend/` directory
2. Update backend API endpoints in `backend/main.py`
3. Test the integration using the provided endpoints

### Model Retraining
1. Update the dataset in `churn-ml-model/`
2. Run `train_model.py` to create a new model
3. Replace `backend/churn_model.pkl` with the new model
4. Restart the backend server

## License

This project is for educational and demonstration purposes.

## Support

For issues or questions, please check the troubleshooting section or verify that all components are properly configured.
