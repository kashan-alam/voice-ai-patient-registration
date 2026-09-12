from datetime import date, datetime
from enum import Enum
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)

from app.utils.validation import (
    validate_date_of_birth,
    validate_insurance_member_id,
    validate_name,
    validate_state,
    validate_us_phone,
    validate_zip_code,
)


class SexEnum(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"
    DECLINE_TO_ANSWER = "Decline to Answer"


class PatientBase(BaseModel):
    """
    Shared patient fields used for creation and updates.
    """

    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)

    date_of_birth: date

    sex: SexEnum

    phone_number: str

    address_line_1: str = Field(..., min_length=1, max_length=200)
    address_line_2: str | None = Field(default=None, max_length=200)

    city: str = Field(..., min_length=1, max_length=100)

    state: str

    zip_code: str

    email: EmailStr | None = None

    insurance_provider: str | None = Field(
        default=None,
        max_length=100,
    )

    insurance_member_id: str | None = Field(
        default=None,
        max_length=100,
    )

    preferred_language: str = Field(
        default="English",
        min_length=1,
        max_length=50,
    )

    emergency_contact_name: str | None = Field(
        default=None,
        max_length=100,
    )

    emergency_contact_phone: str | None = None

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_names(cls, value: str) -> str:
        return validate_name(value)

    @field_validator("date_of_birth")
    @classmethod
    def validate_dob(cls, value: date) -> date:
        return validate_date_of_birth(value)

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        return validate_us_phone(value)

    @field_validator("state")
    @classmethod
    def validate_state_code(cls, value: str) -> str:
        return validate_state(value)

    @field_validator("zip_code")
    @classmethod
    def validate_zip(cls, value: str) -> str:
        return validate_zip_code(value)

    @field_validator("insurance_member_id")
    @classmethod
    def validate_member_id(cls, value: str | None) -> str | None:
        if value is None:
            return None

        return validate_insurance_member_id(value)

    @field_validator("emergency_contact_phone")
    @classmethod
    def validate_emergency_phone(cls, value: str | None) -> str | None:
        if value is None:
            return None

        return validate_us_phone(value)


class PatientCreate(PatientBase):
    """
    Schema used when creating a new patient.
    """

    pass


class PatientUpdate(BaseModel):
    """
    Schema used for partial patient updates.

    Every field is optional because PUT will support partial updates.
    """

    first_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )

    last_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )

    date_of_birth: date | None = None

    sex: SexEnum | None = None

    phone_number: str | None = None

    address_line_1: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )

    address_line_2: str | None = Field(
        default=None,
        max_length=200,
    )

    city: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    state: str | None = None

    zip_code: str | None = None

    email: EmailStr | None = None

    insurance_provider: str | None = Field(
        default=None,
        max_length=100,
    )

    insurance_member_id: str | None = Field(
        default=None,
        max_length=100,
    )

    preferred_language: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )

    emergency_contact_name: str | None = Field(
        default=None,
        max_length=100,
    )

    emergency_contact_phone: str | None = None

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_names(cls, value: str | None) -> str | None:
        if value is None:
            return None

        return validate_name(value)

    @field_validator("date_of_birth")
    @classmethod
    def validate_dob(cls, value: date | None) -> date | None:
        if value is None:
            return None

        return validate_date_of_birth(value)

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, value: str | None) -> str | None:
        if value is None:
            return None

        return validate_us_phone(value)

    @field_validator("state")
    @classmethod
    def validate_state_code(cls, value: str | None) -> str | None:
        if value is None:
            return None

        return validate_state(value)

    @field_validator("zip_code")
    @classmethod
    def validate_zip(cls, value: str | None) -> str | None:
        if value is None:
            return None

        return validate_zip_code(value)

    @field_validator("insurance_member_id")
    @classmethod
    def validate_member_id(cls, value: str | None) -> str | None:
        if value is None:
            return None

        return validate_insurance_member_id(value)

    @field_validator("emergency_contact_phone")
    @classmethod
    def validate_emergency_phone(cls, value: str | None) -> str | None:
        if value is None:
            return None

        return validate_us_phone(value)


class PatientResponse(PatientBase):
    """
    Schema returned by the API.
    """

    patient_id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)