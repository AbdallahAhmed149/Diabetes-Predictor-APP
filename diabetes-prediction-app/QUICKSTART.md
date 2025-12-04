# Quick Start Guide

## 🚀 Super Quick Setup (3 Steps)

### Option 1: Using the Start Script (Easiest)

1. Open the project folder: `d:\ML Algorithms\Logistic Regression\diabetes-prediction-app`
2. Double-click `start.bat`
3. Wait for services to start (2-3 minutes first time)
4. Open browser at <http://localhost:3000>

### Option 2: Using Command Line

```bash
cd "d:\ML Algorithms\Logistic Regression\diabetes-prediction-app"
docker-compose up --build
```

Then open: <http://localhost:3000>

## 📝 First Login

1. Click "Register here"
2. Fill in your details (use role: "doctor" for full access)
3. Login with your credentials

## ✅ What Works Now

✔ **Backend (FastAPI)**

- Complete REST API with all endpoints
- ML model integration with preprocessing
- Authentication (JWT)
- Database models for users, patients, predictions
- Auto-loads ML models on startup

✔ **Frontend (Next.js)**

- Login & Registration pages
- Dashboard home with navigation
- Professional medical-grade UI theme

✔ **Database (PostgreSQL)**

- Complete schema with all 29 prediction fields
- Auto-initialization

✔ **Docker Setup**

- Multi-container orchestration
- One-command startup

## 🔨 Next Steps to Complete

The **core infrastructure is 100% complete**! To finish the full application:

1. **Prediction Form** - Create the 29-field form (5-step wizard)
2. **Patient Management** - List, create, edit patients
3. **Results Page** - Show predictions with risk gauge
4. **History View** - Display past predictions
5. **PDF Generation** - Create downloadable reports

These are **frontend pages only** - the backend API is ready!

## 🎯 Test the Backend API Now

Visit <http://localhost:8000/docs> to:

- Test all API endpoints directly
- Try the prediction endpoint with sample data
- See the ML model working live

## 📋 Sample Prediction Data  

Try this in the API docs (`/api/predictions` endpoint):

```json
{
  "patient_id": 1,
  "age": 45,
  "gender": "Male",
  "ethnicity": "White",
  "education_level": "Graduate",
  "income_level": "Middle",
  "employment_status": "Employed",
  "smoking_status": "Never",
  "alcohol_consumption_per_week": 2,
  "physical_activity_minutes_per_week": 150,
  "diet_score": 7.5,
  "sleep_hours_per_day": 7,
  "screen_time_hours_per_day": 4,
  "family_history_diabetes": false,
  "hypertension_history": false,
  "cardiovascular_history": false,
  "bmi": 26.5,
  "waist_to_hip_ratio": 0.85,
  "systolic_bp": 125,
  "diastolic_bp": 80,
  "heart_rate": 72,
  "cholesterol_total": 200,
  "hdl_cholesterol": 55,
  "ldl_cholesterol": 120,
  "triglycerides": 150,
  "glucose_fasting": 95,
  "glucose_postprandial": 140,
  "insulin_level": 10,
  "hba1c": 5.7,
  "diabetes_risk_score": 25
}
```

## 🛑 Stop the Application

Press `CTRL+C` in the terminal, then:

```bash
docker-compose down
```

---

**Status**: Core application is deployment-ready! Backend + DB fully functional. Frontend needs additional pages for complete UX.
