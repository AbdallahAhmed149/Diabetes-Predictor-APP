from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PredictionInput(BaseModel):
    """Schema for prediction input - all 29 fields"""

    # Demographics (7 fields)
    age: int = Field(..., ge=18, le=120)
    gender: str = Field(..., pattern="^(Male|Female|Other)$")
    ethnicity: str = Field(..., pattern="^(White|Black|Asian|Hispanic|Other)$")
    education_level: str = Field(
        ..., pattern="^(No formal|Highschool|Graduate|Postgraduate)$"
    )
    income_level: str = Field(
        ..., pattern="^(Low|Lower-Middle|Middle|Upper-Middle|High)$"
    )
    employment_status: str = Field(
        ..., pattern="^(Employed|Unemployed|Retired|Student)$"
    )
    smoking_status: str = Field(..., pattern="^(Never|Former|Current)$")

    # Lifestyle (5 fields)
    alcohol_consumption_per_week: float = Field(..., ge=0, le=50)
    physical_activity_minutes_per_week: int = Field(..., ge=0, le=3000)
    diet_score: float = Field(..., ge=0, le=10)
    sleep_hours_per_day: float = Field(..., ge=0, le=24)
    screen_time_hours_per_day: float = Field(..., ge=0, le=24)

    # Medical History (3 fields)
    family_history_diabetes: bool
    hypertension_history: bool
    cardiovascular_history: bool

    # Physical Measurements (5 fields)
    bmi: float = Field(..., ge=10, le=60)
    waist_to_hip_ratio: float = Field(..., ge=0.5, le=1.5)
    systolic_bp: int = Field(..., ge=70, le=250)
    diastolic_bp: int = Field(..., ge=40, le=150)
    heart_rate: int = Field(..., ge=30, le=200)

    # Lab Results (9 fields)
    cholesterol_total: float = Field(..., ge=100, le=500)
    hdl_cholesterol: float = Field(..., ge=20, le=150)
    ldl_cholesterol: float = Field(..., ge=30, le=400)
    triglycerides: float = Field(..., ge=25, le=500)
    glucose_fasting: float = Field(..., ge=50, le=300)
    glucose_postprandial: float = Field(..., ge=60, le=400)
    insulin_level: float = Field(..., ge=1, le=50)
    hba1c: float = Field(..., ge=3, le=15)
    diabetes_risk_score: float = Field(..., ge=0, le=100)


class PredictionCreate(PredictionInput):
    """Schema for creating a prediction"""

    patient_id: int


class PredictionResponse(BaseModel):
    """Schema for prediction response"""

    id: int
    patient_id: int
    doctor_id: Optional[int]

    # Prediction results
    risk_probability: float
    risk_level: str
    prediction_class: int
    risk_interpretation: str

    created_at: datetime

    class Config:
        from_attributes = True


class PredictionDetail(PredictionResponse):
    """Schema for detailed prediction with all input fields"""

    # All input fields
    age: int
    gender: str
    ethnicity: str
    education_level: str
    income_level: str
    employment_status: str
    smoking_status: str
    alcohol_consumption_per_week: float
    physical_activity_minutes_per_week: int
    diet_score: float
    sleep_hours_per_day: float
    screen_time_hours_per_day: float
    family_history_diabetes: bool
    hypertension_history: bool
    cardiovascular_history: bool
    bmi: float
    waist_to_hip_ratio: float
    systolic_bp: int
    diastolic_bp: int
    heart_rate: int
    cholesterol_total: float
    hdl_cholesterol: float
    ldl_cholesterol: float
    triglycerides: float
    glucose_fasting: float
    glucose_postprandial: float
    insulin_level: float
    hba1c: float
    diabetes_risk_score: float


