import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Patient
from app.schemas.patient import PatientCreate, PatientUpdate


def create_patient(
    db: Session,
    patient_data: PatientCreate,
) -> Patient:
    """
    Create and persist a new patient.
    """

    patient = Patient(
        **patient_data.model_dump(),
        patient_id=uuid.uuid4(),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    db.add(patient)
    db.commit()
    db.refresh(patient)

    return patient


def get_patient(
    db: Session,
    patient_id: uuid.UUID,
) -> Patient | None:
    """
    Retrieve an active patient by UUID.

    Soft-deleted patients are not returned.
    """

    statement = select(Patient).where(
        Patient.patient_id == patient_id,
        Patient.deleted_at.is_(None),
    )

    return db.scalar(statement)


def list_patients(
    db: Session,
    last_name: str | None = None,
    date_of_birth=None,
    phone_number: str | None = None,
) -> list[Patient]:
    """
    Return active patients.

    Optional filters:
    - last_name
    - date_of_birth
    - phone_number
    """

    statement = select(Patient).where(
        Patient.deleted_at.is_(None)
    )

    if last_name:
        statement = statement.where(
            Patient.last_name.ilike(last_name)
        )

    if date_of_birth:
        statement = statement.where(
            Patient.date_of_birth == date_of_birth
        )

    if phone_number:
        statement = statement.where(
            Patient.phone_number == phone_number
        )

    statement = statement.order_by(Patient.created_at.desc())

    return list(db.scalars(statement).all())


def update_patient(
    db: Session,
    patient: Patient,
    patient_data: PatientUpdate,
) -> Patient:
    """
    Update an existing patient.

    Only fields explicitly supplied by the caller are changed.
    """

    update_data = patient_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(patient, field, value)

    patient.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(patient)

    return patient


def delete_patient(
    db: Session,
    patient: Patient,
) -> Patient:
    """
    Soft-delete a patient.

    The database row remains intact.
    """

    patient.deleted_at = datetime.now(timezone.utc)
    patient.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(patient)

    return patient