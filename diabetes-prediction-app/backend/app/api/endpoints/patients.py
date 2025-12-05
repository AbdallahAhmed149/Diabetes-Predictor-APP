from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.patient import PatientCreate, PatientUpdate, Patient as PatientSchema
from app.models.patient import Patient as PatientModel
from app.models.user import User as UserModel
from app.api.endpoints.auth import get_current_user

router = APIRouter(prefix="/patients", tags=["patients"])


@router.post("/", response_model=PatientSchema, status_code=status.HTTP_201_CREATED)
def create_patient(
    patient_data: PatientCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new patient profile"""
    # Check if patient code already exists
    existing_patient = (
        db.query(PatientModel)
        .filter(PatientModel.patient_code == patient_data.patient_code)
        .first()
    )

    if existing_patient:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Patient code already exists",
        )

    new_patient = PatientModel(**patient_data.model_dump())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient


@router.get("/", response_model=List[PatientSchema])
def list_patients(
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all patients (doctors) or own profile (patients)"""
    if current_user.role.value == "doctor":
        patients = db.query(PatientModel).offset(skip).limit(limit).all()
    else:
        patients = (
            db.query(PatientModel).filter(PatientModel.user_id == current_user.id).all()
        )

    return patients


@router.get("/{patient_id}", response_model=PatientSchema)
def get_patient(
    patient_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get patient details by ID"""
    patient = db.query(PatientModel).filter(PatientModel.id == patient_id).first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
        )

    # Check access for patients
    if current_user.role.value == "patient" and patient.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )

    return patient


@router.put("/{patient_id}", response_model=PatientSchema)
def update_patient(
    patient_id: int,
    patient_update: PatientUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update patient information"""
    patient = db.query(PatientModel).filter(PatientModel.id == patient_id).first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
        )

    # Check access for patients
    if current_user.role.value == "patient" and patient.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )

    # Update fields
    update_data = patient_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(patient, field, value)

    db.commit()
    db.refresh(patient)

    return patient


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(
    patient_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a patient (doctors only)"""
    if current_user.role.value != "doctor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only doctors can delete patients",
        )

    patient = db.query(PatientModel).filter(PatientModel.id == patient_id).first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
        )

    db.delete(patient)
    db.commit()

