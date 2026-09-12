import uuid
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.patient import (
    PatientCreate,
    PatientResponse,
    PatientUpdate,
)
from app.services.patient_service import (
    create_patient,
    delete_patient,
    get_patient,
    list_patients,
    update_patient,
)
from app.utils.validation import validate_us_phone


router = APIRouter(
    prefix="/patients",
    tags=["Patients"],
)


def success_response(data):
    """
    Create the standard successful API response.
    """
    return {
        "data": data,
        "error": None,
    }


def error_response(message: str):
    """
    Create the standard API error response.
    """
    return {
        "data": None,
        "error": {
            "message": message,
        },
    }


@router.post(
    "",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
)
def create_patient_endpoint(
    patient_data: PatientCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new patient.
    """

    patient = create_patient(
        db=db,
        patient_data=patient_data,
    )

    return success_response(
        PatientResponse.model_validate(patient)
    )


@router.get(
    "",
    response_model=dict,
)
def get_patients(
    last_name: str | None = Query(
        default=None,
        max_length=50,
    ),
    date_of_birth: date | None = None,
    phone_number: str | None = None,
    db: Session = Depends(get_db),
):
    """
    Return active patients with optional filters.
    """

    normalized_phone = None

    if phone_number:
        try:
            normalized_phone = validate_us_phone(phone_number)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=error_response(str(exc)),
            )

    patients = list_patients(
        db=db,
        last_name=last_name,
        date_of_birth=date_of_birth,
        phone_number=normalized_phone,
    )

    data = [
        PatientResponse.model_validate(patient)
        for patient in patients
    ]

    return success_response(data)


@router.get(
    "/{patient_id}",
    response_model=dict,
)
def get_patient_endpoint(
    patient_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    """
    Return a single active patient.
    """

    patient = get_patient(
        db=db,
        patient_id=patient_id,
    )

    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response("Patient not found"),
        )

    return success_response(
        PatientResponse.model_validate(patient)
    )


@router.put(
    "/{patient_id}",
    response_model=dict,
)
def update_patient_endpoint(
    patient_id: uuid.UUID,
    patient_data: PatientUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an existing active patient.
    """

    patient = get_patient(
        db=db,
        patient_id=patient_id,
    )

    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response("Patient not found"),
        )

    updated_patient = update_patient(
        db=db,
        patient=patient,
        patient_data=patient_data,
    )

    return success_response(
        PatientResponse.model_validate(updated_patient)
    )


@router.delete(
    "/{patient_id}",
    response_model=dict,
)
def delete_patient_endpoint(
    patient_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    """
    Soft-delete a patient.
    """

    patient = get_patient(
        db=db,
        patient_id=patient_id,
    )

    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response("Patient not found"),
        )

    deleted_patient = delete_patient(
        db=db,
        patient=patient,
    )

    return success_response(
        PatientResponse.model_validate(deleted_patient)
    )