from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.prediction import (
    PredictionCreate,
    PredictionResponse,
    PredictionDetail,
)
from app.models.prediction import Prediction as PredictionModel
from app.models.patient import Patient as PatientModel
from app.models.user import User as UserModel
from app.api.endpoints.auth import get_current_user
from app.ml.predictor import get_predictor
from app.utils.pdf_generator import generate_prediction_report

router = APIRouter(prefix="/predictions", tags=["Predictions"])


@router.post(
    "/", response_model=PredictionResponse, status_code=status.HTTP_201_CREATED
)
def create_prediction(
    prediction_data: PredictionCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new diabetes prediction"""
    
    # ADDED: Validate that the patient exists
    patient = db.query(PatientModel).filter(
        PatientModel.id == prediction_data.patient_id
    ).first()
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID {prediction_data.patient_id} not found. Please ensure you have a patient record created."
        )
    
    # ADDED: For patients, verify they're making predictions for themselves
    if current_user.role.value == "patient":
        # Check if the patient_id belongs to the current user
        if patient.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only create predictions for your own patient record."
            )

    # Get predictor
    predictor = get_predictor()

    # Convert prediction data to dict
    input_dict = prediction_data.model_dump(exclude={"patient_id"})

    # Make prediction
    try:
        result = predictor.predict(input_dict)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )

    # Create prediction record
    new_prediction = PredictionModel(
        patient_id=prediction_data.patient_id,
        doctor_id=current_user.id if current_user.role.value == "doctor" else None,
        **input_dict,
        risk_probability=result["risk_probability"],
        risk_level=result["risk_level"],
        prediction_class=result["prediction_class"],
    )

    db.add(new_prediction)
    db.commit()
    db.refresh(new_prediction)

    # Add risk interpretation to response
    response_dict = {
        **new_prediction.__dict__,
        "risk_interpretation": result["risk_interpretation"],
    }

    return PredictionResponse(**response_dict)


@router.get("/", response_model=List[PredictionResponse])
def list_predictions(
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all predictions (filtered by role)"""
    query = db.query(PredictionModel)

    # If patient, show only their predictions
    if current_user.role.value == "patient":
        # Find patient record for this user
        patient = db.query(PatientModel).filter(
            PatientModel.user_id == current_user.id
        ).first()
        
        if not patient:
            # IMPROVED: Return empty list instead of error for better UX
            return []
        
        query = query.filter(PredictionModel.patient_id == patient.id)

    predictions = (
        query.order_by(PredictionModel.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    # Add risk interpretation
    predictor = get_predictor()
    results = []
    for pred in predictions:
        results.append(
            PredictionResponse(
                **pred.__dict__,
                risk_interpretation=predictor._get_risk_interpretation(
                    pred.risk_level, pred.risk_probability / 100
                ),
            )
        )

    return results


@router.get("/{prediction_id}", response_model=PredictionDetail)
def get_prediction(
    prediction_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get prediction details by ID"""
    prediction = (
        db.query(PredictionModel).filter(PredictionModel.id == prediction_id).first()
    )

    if not prediction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Prediction not found"
        )

    # Check access
    if current_user.role.value == "patient":
        patient = db.query(PatientModel).filter(
            PatientModel.user_id == current_user.id
        ).first()
        
        if not patient or prediction.patient_id != patient.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
            )

    predictor = get_predictor()
    return PredictionDetail(
        **prediction.__dict__,
        risk_interpretation=predictor._get_risk_interpretation(
            prediction.risk_level, prediction.risk_probability / 100
        ),
    )


@router.get("/patient/{patient_id}", response_model=List[PredictionResponse])
def get_patient_predictions(
    patient_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all predictions for a specific patient"""
    # Check access
    if current_user.role.value == "patient":
        patient = db.query(PatientModel).filter(
            PatientModel.user_id == current_user.id
        ).first()
        
        if not patient or patient.id != patient_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
            )

    predictions = (
        db.query(PredictionModel)
        .filter(PredictionModel.patient_id == patient_id)
        .order_by(PredictionModel.created_at.desc())
        .all()
    )

    predictor = get_predictor()
    results = []
    for pred in predictions:
        results.append(
            PredictionResponse(
                **pred.__dict__,
                risk_interpretation=predictor._get_risk_interpretation(
                    pred.risk_level, pred.risk_probability / 100
                ),
            )
        )

    return results


@router.get("/{prediction_id}/report")
def download_prediction_report(
    prediction_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Download PDF report for a specific prediction"""

    # Get prediction
    prediction = (
        db.query(PredictionModel).filter(PredictionModel.id == prediction_id).first()
    )

    if not prediction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Prediction not found"
        )

    # Check authorization
    if current_user.role.value == "patient":
        # Patients can only download their own predictions
        patient = (
            db.query(PatientModel)
            .filter(PatientModel.id == prediction.patient_id)
            .first()
        )
        if not patient or patient.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this prediction",
            )

    # Get patient data
    patient = (
        db.query(PatientModel).filter(PatientModel.id == prediction.patient_id).first()
    )

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
        )

    # Prepare prediction data dict
    prediction_dict = {
        "id": prediction.id,
        "age": prediction.age,
        "gender": prediction.gender,
        "ethnicity": prediction.ethnicity,
        "education_level": prediction.education_level,
        "income_level": prediction.income_level,
        "employment_status": prediction.employment_status,
        "smoking_status": prediction.smoking_status,
        "alcohol_consumption_per_week": prediction.alcohol_consumption_per_week,
        "physical_activity_minutes_per_week": prediction.physical_activity_minutes_per_week,
        "diet_score": prediction.diet_score,
        "sleep_hours_per_day": prediction.sleep_hours_per_day,
        "screen_time_hours_per_day": prediction.screen_time_hours_per_day,
        "family_history_diabetes": prediction.family_history_diabetes,
        "hypertension_history": prediction.hypertension_history,
        "cardiovascular_history": prediction.cardiovascular_history,
        "bmi": prediction.bmi,
        "waist_to_hip_ratio": prediction.waist_to_hip_ratio,
        "systolic_bp": prediction.systolic_bp,
        "diastolic_bp": prediction.diastolic_bp,
        "heart_rate": prediction.heart_rate,
        "cholesterol_total": prediction.cholesterol_total,
        "hdl_cholesterol": prediction.hdl_cholesterol,
        "ldl_cholesterol": prediction.ldl_cholesterol,
        "triglycerides": prediction.triglycerides,
        "glucose_fasting": prediction.glucose_fasting,
        "glucose_postprandial": prediction.glucose_postprandial,
        "insulin_level": prediction.insulin_level,
        "hba1c": prediction.hba1c,
        "diabetes_risk_score": prediction.diabetes_risk_score,
        "risk_probability": prediction.risk_probability,
        "risk_level": prediction.risk_level,
    }

    # Add risk interpretation
    predictor = get_predictor()
    prediction_dict["risk_interpretation"] = predictor._get_risk_interpretation(
        prediction.risk_level, prediction.risk_probability / 100
    )

    # Prepare patient data dict
    patient_dict = {
        "patient_code": patient.patient_code,
        "date_of_birth": str(patient.date_of_birth) if patient.date_of_birth else "N/A",
        "phone": patient.phone or "N/A",
        "address": patient.address or "N/A",
        "emergency_contact": patient.emergency_contact or "N/A",
    }

    # Generate PDF
    pdf_buffer = generate_prediction_report(prediction_dict, patient_dict)

    # Return PDF as streaming response
    filename = f"diabetes_report_{patient.patient_code}_{prediction.id}.pdf"

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
