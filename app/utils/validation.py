import re
from datetime import date


# Valid US state and territory abbreviations.
US_STATE_CODES = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE",
    "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS",
    "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS",
    "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY",
    "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV",
    "WI", "WY", "DC",
}


def validate_name(value: str) -> str:
    """
    Validate a person's name.

    Allows alphabetic characters, spaces, hyphens, and apostrophes.
    """
    value = value.strip()

    if not value:
        raise ValueError("Name cannot be empty.")

    if len(value) > 50:
        raise ValueError("Name must be 50 characters or fewer.")

    if not re.fullmatch(r"[A-Za-z]+(?:[ '\-][A-Za-z]+)*", value):
        raise ValueError(
            "Name may contain only letters, spaces, hyphens, and apostrophes."
        )

    return value


def validate_us_phone(value: str) -> str:
    """
    Validate and normalize a US phone number.

    Accepts common formatting such as:
    415-555-1234
    (415) 555-1234
    4155551234

    Stores the normalized 10-digit number.
    """
    digits = re.sub(r"\D", "", value)

    # Allow +1XXXXXXXXXX.
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]

    if len(digits) != 10:
        raise ValueError("Phone number must contain a valid US 10-digit number.")

    return digits


def validate_state(value: str) -> str:
    """
    Validate a US state abbreviation.
    """
    value = value.strip().upper()

    if value not in US_STATE_CODES:
        raise ValueError("State must be a valid US state abbreviation.")

    return value


def validate_zip_code(value: str) -> str:
    """
    Validate US ZIP code.

    Accepts:
    12345
    12345-6789
    """
    value = value.strip()

    if not re.fullmatch(r"\d{5}(?:-\d{4})?", value):
        raise ValueError("ZIP code must be 5 digits or ZIP+4.")

    return value


def validate_date_of_birth(value: date) -> date:
    """
    Validate that the date of birth is not in the future.
    """
    if value > date.today():
        raise ValueError("Date of birth cannot be in the future.")

    return value


def validate_insurance_member_id(value: str) -> str:
    """
    Validate insurance member ID.

    Allows letters, numbers, hyphens, and underscores.
    """
    value = value.strip()

    if not value:
        raise ValueError("Insurance member ID cannot be empty.")

    if len(value) > 100:
        raise ValueError("Insurance member ID must be 100 characters or fewer.")

    if not re.fullmatch(r"[A-Za-z0-9_-]+", value):
        raise ValueError(
            "Insurance member ID may contain only letters, numbers, "
            "hyphens, and underscores."
        )

    return value