<div align="center">

# 🏥 Diabetes Risk Prediction System

### AI-Powered Medical Application for Diabetes Risk Assessment

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Frontend-Next.js%2014-000000?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Containerized-Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)

[Features](#-features) • [Quick Start](#-quick-start) • [Tech Stack](#%EF%B8%8F-technology-stack) • [API Docs](#-api-documentation) • [Contributing](#-contributing)

---

</div>

## 📖 Overview

A comprehensive, production-ready web application that leverages **Machine Learning** to assess diabetes risk based on 29 comprehensive health parameters. Built with modern technologies and designed for healthcare professionals and patients alike.

### 🎯 Key Highlights

- 🧠 **Machine Learning Powered** - Logistic Regression model with 29-parameter risk assessment
- 🔐 **Secure Authentication** - JWT-based auth with role-based access control (Doctor/Patient)
- 📊 **Comprehensive Dashboard** - Real-time predictions, patient management, and history tracking
- 🎨 **Beautiful UI/UX** - Modern, responsive design with custom form elements and gradients
- 🐳 **Fully Containerized** - One-command deployment with Docker Compose
- 📈 **RESTful API** - Well-documented FastAPI backend with automatic Swagger docs

---

## ✨ Features

### For Doctors 🩺

- ✅ **Patient Management** - Create, view, update, and delete patient records
- ✅ **Multi-Patient Dashboard** - Manage multiple patients from one interface
- ✅ **Comprehensive Risk Assessment** - 29-parameter diabetes prediction model
- ✅ **Prediction History** - Track all past assessments with timestamps
- ✅ **PDF Reports** - Generate downloadable assessment reports

### For Patients 👤

- ✅ **Personal Dashboard** - View own prediction history and risk status
- ✅ **Self-Assessment** - Submit health data for AI-powered risk analysis
- ✅ **Risk Visualization** - Color-coded risk levels (Low/Medium/High)
- ✅ **Health Tracking** - Monitor risk trends over time

### Technical Features ⚙️

- ✅ **Robust ML Pipeline** - OneHotEncoding → Polynomial Features → Standard Scaling → Logistic Regression
- ✅ **Real-time Predictions** - Instant risk assessment (<100ms)
- ✅ **Data Persistence** - PostgreSQL database with SQLAlchemy ORM
- ✅ **Input Validation** - Pydantic schemas for data integrity
- ✅ **Error Handling** - Graceful error management with user-friendly messages

---

## 📊 Risk Classification System

The ML model outputs probability scores (0-100%) categorized into three risk levels:

| Probability Range | Risk Level | Visual Indicator | Recommendation |
|-------------------|------------|------------------|----------------|
| **0-30%** | 🟢 **Low Risk** | Green gradient | Continue healthy lifestyle, routine check-ups |
| **30-70%** | 🟡 **Medium Risk** | Yellow/Orange gradient | Lifestyle modifications, regular monitoring |
| **70-100%** | 🔴 **High Risk** | Red gradient | Immediate medical consultation recommended |

---

## 🚀 Quick Start

### Prerequisites

Ensure you have the following installed:

- [Docker](https://www.docker.com/get-started) (20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (2.0+)
- (Optional) [Node.js 18+](https://nodejs.org/) for local frontend development
- (Optional) [Python 3.11+](https://www.python.org/) for local backend development

### Installation & Setup

#### Option 1: Docker (Recommended) 🐳

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/diabetes-prediction-app.git
cd diabetes-prediction-app

# Start all services with Docker Compose
docker-compose up -d

# View logs (optional)
docker-compose logs -f
```

**That's it!** The application is now running:

- 🌐 **Frontend**: [http://localhost:3000](http://localhost:3000)
- 🔧 **Backend API**: [http://localhost:8000](http://localhost:8000)
- 📚 **API Docs (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- 📖 **API Docs (ReDoc)**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

#### Option 2: Local Development

<details>
<summary>Click to expand local development setup</summary>

**Backend Setup:**

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql://user:pass@localhost:5432/diabetes_db"
export SECRET_KEY="your-secret-key-here"

# Run development server
uvicorn app.main:app --reload --port 8000
```

**Frontend Setup:**

```bash
cd frontend

# Install dependencies
npm install

# Set environment variables
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Run development server
npm run dev
```

</details>

### Default Test Credentials

For testing purposes, use these credentials:

**Doctor Account:**

```
Email: doctor@test.com
Password: password123
```

**Patient Account:**

```
Email: patient@test.com
Password: password123
```

> ⚠️ **Security Note**: Change these credentials in production!

---

## 🩺 Assessment Parameters (29 Fields)

The ML model evaluates diabetes risk using 29 comprehensive health parameters:

### 👤 Demographics (7 Parameters)

| Parameter | Type | Examples |
|-----------|------|----------|
| Age | Numeric | 18-100 years |
| Gender | Categorical | Male, Female |
| Ethnicity | Categorical | Caucasian, African American, Hispanic, Asian, Other |
| Education Level | Categorical | No Formal, High School, Graduate, Postgraduate |
| Income Level | Categorical | Low, Middle, High |
| Employment Status | Categorical | Employed, Unemployed, Self-Employed, Retired |
| Smoking Status | Categorical | Never, Former, Current |

### 📏 Physical Measurements (5 Parameters)

- **BMI** (Body Mass Index): 15-50 kg/m²
- **Waist-to-Hip Ratio**: 0.5-1.5
- **Systolic Blood Pressure**: 80-200 mmHg
- **Diastolic Blood Pressure**: 50-130 mmHg
- **Heart Rate**: 40-150 bpm

### 🧪 Laboratory Results (9 Parameters)

- **Fasting Glucose**: 70-200 mg/dL
- **Postprandial Glucose**: 80-300 mg/dL
- **HbA1c** (Glycated Hemoglobin): 4-12%
- **Insulin Level**: 2-30 μU/mL
- **Total Cholesterol**: 100-400 mg/dL
- **HDL Cholesterol**: 20-100 mg/dL
- **LDL Cholesterol**: 50-250 mg/dL
- **Triglycerides**: 50-500 mg/dL
- **Diabetes Risk Score**: 0-100

### 🏃 Lifestyle Factors (5 Parameters)

- **Alcohol Consumption**: 0-50 drinks/week
- **Physical Activity**: 0-500 minutes/week
- **Diet Score**: 0-10 (quality rating)
- **Sleep Hours**: 3-12 hours/day
- **Screen Time**: 0-16 hours/day

### 🏥 Medical History (3 Boolean Parameters)

- ✅ Family History of Diabetes
- ✅ History of Hypertension  
- ✅ Cardiovascular Disease History

---

## 🛠️ Technology Stack

### Backend Architecture

| Technology | Purpose | Version |
|------------|---------|---------|
| **FastAPI** | Web framework | 0.109+ |
| **PostgreSQL** | Relational database | 15+ |
| **SQLAlchemy** | ORM | 2.0+ |
| **Pydantic** | Data validation | 2.9+ |
| **scikit-learn** | ML library | 1.4+ |
| **pandas** | Data manipulation | 2.1+ |
| **numpy** | Numerical computing | 1.24+ |
| **ReportLab** | PDF generation | 4.0+ |
| **bcrypt** | Password hashing | 4.1+ |
| **python-jose** | JWT handling | 3.3+ |

### Frontend Technologies

| Technology | Purpose | Version |
|------------|---------|---------|
| **Next.js** | React framework | 14.2+ |
| **React** | UI library | 18+ |
| **TypeScript** | Type safety | 5.0+ |
| **Axios** | HTTP client | 1.6+ |
| **CSS3** | Custom styling | - |

### DevOps & Infrastructure

- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Uvicorn** - ASGI server
- **Nginx** (optional) - Reverse proxy for production

---

## 📁 Project Structure

```
diabetes-prediction-app/
│
├── backend/                          # FastAPI Backend
│   ├── app/
│   │   ├── api/
│   │   │   └── endpoints/
│   │   │       ├── auth.py           # Authentication endpoints
│   │   │       ├── patients.py       # Patient CRUD operations
│   │   │       └── predictions.py    # ML prediction endpoints
│   │   ├── core/
│   │   │   ├── config.py             # Application configuration
│   │   │   ├── database.py           # Database connection
│   │   │   └── security.py           # JWT & password utilities
│   │   ├── ml/
│   │   │   ├── models/               # Pretrained ML models
│   │   │   ├── load_models.py        # Model loading
│   │   │   ├── predictor.py          # Prediction logic
│   │   │   └── preprocessor.py       # Feature engineering
│   │   ├── models/                   # SQLAlchemy models
│   │   │   ├── user.py
│   │   │   ├── patient.py
│   │   │   └── prediction.py
│   │   ├── schemas/                  # Pydantic schemas
│   │   │   ├── user.py
│   │   │   ├── patient.py
│   │   │   └── prediction.py
│   │   └── utils/
│   │       └── pdf_generator.py      # PDF report generation
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/                         # Next.js Frontend
│   ├── src/
│   │   ├── app/
│   │   │   ├── (auth)/
│   │   │   │   ├── login/            # Login page
│   │   │   │   └── register/         # Registration page
│   │   │   ├── dashboard/
│   │   │   │   ├── page.tsx          # Main dashboard
│   │   │   │   ├── predict/          # Risk assessment form
│   │   │   │   ├── history/          # Prediction history
│   │   │   │   └── patients/         # Patient management (doctors)
│   │   │   ├── globals.css           # Global styles
│   │   │   └── layout.tsx            # Root layout
│   │   └── lib/
│   │       └── api.ts                # API client & interceptors
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.js
│   └── Dockerfile
│
├── database/
│   └── init.sql                      # Database initialization script
│
├── docker-compose.yml                # Multi-container configuration
├── .env.example                      # Environment variables template
├── .gitignore
├── README.md
└── LICENSE
```

---

## 🔧 API Documentation

### Interactive Documentation

FastAPI provides auto-generated interactive API documentation:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Core API Endpoints

#### Authentication Endpoints

```http
POST   /api/auth/register        # Register new user
POST   /api/auth/login           # Login & get JWT token
GET    /api/auth/me              # Get current user info
```

**Example Request (Register):**

```json
{
  "email": "doctor@example.com",
  "password": "SecurePass123!",
  "full_name": "Dr. John Smith",
  "role": "doctor"
}
```

#### Patient Management

```http
GET    /api/patients/            # List all patients
POST   /api/patients/            # Create new patient
GET    /api/patients/{id}/       # Get specific patient
PUT    /api/patients/{id}/       # Update patient info
DELETE /api/patients/{id}/       # Delete patient
```

#### Prediction Endpoints

```http
POST   /api/predictions/                    # Create new prediction
GET    /api/predictions/                    # List predictions
GET    /api/predictions/{id}/               # Get specific prediction
GET    /api/predictions/{id}/report         # Download PDF report
GET    /api/predictions/patient/{patient_id}/ # Get patient's predictions
```

---

## 🔐 Security Features

This application implements multiple security layers:

| Feature | Implementation |
|---------|----------------|
| 🔑 **Authentication** | JWT tokens with configurable expiration |
| 🔒 **Password Security** | bcrypt hashing with salt rounds |
| 🛡️ **Authorization** | Role-based access control (RBAC) |
| ✅ **Input Validation** | Pydantic schema validation |
| 🚫 **SQL Injection Protection** | SQLAlchemy ORM with parameterized queries |
| 🔐 **CORS Configuration** | Restricted origins in production |

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

### ⭐ Star this project if you find it useful

**Built with ❤️ for better healthcare and AI-powered medicine**

[⬆ Back to Top](#-diabetes-risk-prediction-system)

</div>
