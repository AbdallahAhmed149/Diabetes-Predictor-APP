from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"))
    doctor_id = Column(Integer, ForeignKey("users.id"))

    # Demographics (7 fields)
    age = Column(Integer)
    gender = Column(String)
    ethnicity = Column(String)
    education_level = Column(String)
    income_level = Column(String)
    employment_status = Column(String)
    smoking_status = Column(String)

    # Lifestyle (5 fields)
    alcohol_consumption_per_week = Column(Float)
    physical_activity_minutes_per_week = Column(Integer)
    diet_score = Column(Float)
    sleep_hours_per_day = Column(Float)
    screen_time_hours_per_day = Column(Float)

    # Medical History (3 fields)
    family_history_diabetes = Column(Boolean)
    hypertension_history = Column(Boolean)
    cardiovascular_history = Column(Boolean)

    # Physical Measurements (5 fields)
    bmi = Column(Float)
    waist_to_hip_ratio = Column(Float)
    systolic_bp = Column(Integer)
    diastolic_bp = Column(Integer)
    heart_rate = Column(Integer)

    # Lab Results (9 fields)
    cholesterol_total = Column(Float)
    hdl_cholesterol = Column(Float)
    ldl_cholesterol = Column(Float)
    triglycerides = Column(Float)
    glucose_fasting = Column(Float)
    glucose_postprandial = Column(Float)
    insulin_level = Column(Float)
    hba1c = Column(Float)
    diabetes_risk_score = Column(Float)

    # Prediction Results
    risk_probability = Column(Float)
    risk_level = Column(String)  # Low, Medium, High
    prediction_class = Column(Integer)  # 0 or 1

    created_at = Column(DateTime(timezone=True), server_default=func.now())
