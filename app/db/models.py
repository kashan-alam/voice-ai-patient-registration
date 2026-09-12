import uuid
from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, Index, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Patient(Base):
    """
    SQLAlchemy model representing a registered patient.
    """

    __tablename__ = "patients"

    patient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    first_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    date_of_birth: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    sex: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    phone_number: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    address_line_1: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    address_line_2: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    state: Mapped[str] = mapped_column(
        String(2),
        nullable=False,
    )

    zip_code: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    insurance_provider: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    insurance_member_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    preferred_language: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="English",
    )

    emergency_contact_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    emergency_contact_phone: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


# Useful indexes for patient lookup.
Index("ix_patients_last_name", Patient.last_name)
Index("ix_patients_date_of_birth", Patient.date_of_birth)
Index("ix_patients_phone_number", Patient.phone_number)