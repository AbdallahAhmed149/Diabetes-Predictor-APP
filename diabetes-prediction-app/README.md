# 🏥 Diabetes Risk Prediction Application

A comprehensive medical-grade web application for diabetes risk prediction using Machine Learning. Built with Next.js, FastAPI, and PostgreSQL.

![Diabetes Prediction](https://img.shields.io/badge/ML-Logistic%20Regression-blue)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-green)
![Next.js](https://img.shields.io/badge/Frontend-Next.js%2014-black)
![Docker](https://img.shields.io/badge/Containerized-Docker-blue)

---

## 🎯 Features

- ✅ **User Authentication** - Secure JWT-based auth with role management (Doctor/Patient)
- ✅ **Patient Management** - Full CRUD operations for patient records
- ✅ **Risk Prediction** - ML-powered diabetes risk assessment with 29 health parameters
- ✅ **Prediction History** - Track and visualize past assessments
- ✅ **Role-Based Access** - Different views for doctors and patients
- ✅ **Beautiful UI** - Modern, responsive design with color-coded risk levels

---

## 📊 Risk Classification

The application uses a **Logistic Regression** model that outputs probabilities (0-100%):

| Probability | Risk Level | Color | Recommendation |
|------------|------------|-------|----------------|
| < 30% | **Low Risk** 🟢 | Green | Continue healthy lifestyle |
| 30-70% | **Medium Risk** 🟡 | Yellow | Lifestyle modifications needed |
| > 70% | **High Risk** 🔴 | Red | Consult healthcare provider |

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Run with Docker (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/diabetes-prediction-app.git
cd diabetes-prediction-app

# 2. Start all services
docker-compose up -d

# 3. Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Default Credentials

```
Email: doctor@test.com
Password: password123
```

---

## 📁 Project Structure

```
diabetes-prediction-app/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/endpoints/  # API routes
│   │   ├── ml/             # ML models & preprocessing
│   │   ├── models/         # SQLAlchemy models
│   │   └── schemas/        # Pydantic schemas
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # Next.js frontend
│   ├── src/app/
│   │   ├── (auth)/        # Login & Register
│   │   └── dashboard/     # Main application
│   ├── package.json
│   └── Dockerfile
├── database/
│   └── init.sql           # Database initialization
├── docker-compose.yml
└── README.md
```

---

## 🩺 Prediction Parameters (29 Fields)

### Demographics (6)

- Age, Gender, Ethnicity
- Education Level, Income Level, Employment Status

### Physical Measurements (5)

- BMI, Waist-Hip Ratio, Heart Rate
- Systolic BP, Diastolic BP

### Lab Results (8)

- Fasting Glucose, Postprandial Glucose
- HbA1c, Insulin Level
- Cholesterol (Total, HDL, LDL), Triglycerides

### Lifestyle Factors (7)

- Smoking Status, Alcohol Consumption
- Physical Activity, Diet Score
- Sleep Hours, Screen Time

### Medical History (3)

- Family History of Diabetes
- Hypertension History
- Cardiovascular History

---

## 🛠️ Technology Stack

### Backend

- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ML:** Scikit-learn (Logistic Regression)
- **Auth:** JWT with bcrypt
- **Container:** Docker

### Frontend

- **Framework:** Next.js 14 + React
- **Language:** TypeScript
- **Styling:** CSS
- **API Client:** Axios

### ML Pipeline

1. OneHotEncoder for categorical features
2. PolynomialFeatures for feature engineering
3. StandardScaler for normalization  
4. Logistic Regression for classification

---

## 📸 Screenshots

### Login Page

![Login](docs/screenshots/login.png)

### Prediction Form

![Prediction Form](docs/screenshots/predict_form.png)

### Results Display

![Results](docs/screenshots/results.png)

### History Dashboard

![History](docs/screenshots/history.png)

---

## 🔧 Development Setup

### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

---

## 🧪 API Documentation

Interactive API docs available at:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

### Key Endpoints

**Authentication**

```http
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me
```

**Patients**

```http
GET    /api/patients/
POST   /api/patients/
PUT    /api/patients/{id}/
DELETE /api/patients/{id}/
```

**Predictions**

```http
POST /api/predictions/
GET  /api/predictions/
```

---

## 🔐 Security Features

- ✅ JWT-based authentication
- ✅ Password hashing with bcrypt
- ✅ HTTP-only cookies
- ✅ Role-based access control
- ✅ Input validation with Pydantic
- ✅ SQL injection protection with SQLAlchemy ORM

---

## 🐳 Docker Services

| Service | Port | Description |
|---------|------|-------------|
| `frontend` | 3000 | Next.js application |
| `backend` | 8000 | FastAPI server |
| `db` | 5432 | PostgreSQL database |

---

## 📊 Database Schema

### Users Table

- `id`, `email`, `full_name`, `hashed_password`, `role`

### Patients Table

- `id`, `patient_code`, `date_of_birth`, `phone`, `address`, `emergency_contact`, `user_id`

### Predictions Table

- All 29 input parameters
- `risk_probability`, `risk_level`, `prediction_class`
- `patient_id`, `doctor_id`, `created_at`

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

Your Name - [@yourhandle](https://github.com/yourhandle)

Project Link: [https://github.com/yourhandle/diabetes-prediction-app](https://github.com/yourhandle/diabetes-prediction-app)

---

## 🙏 Acknowledgments

- Logistic Regression model trained on diabetes dataset
- FastAPI for the excellent web framework
- Next.js team for the amazing React framework
- Docker for containerization

---

**Built with ❤️ for better healthcare**
