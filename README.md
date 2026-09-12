# Voice AI Patient Registration System

A voice-enabled patient registration system built with Vapi, FastAPI, PostgreSQL, SQLAlchemy, and an HTML/JavaScript dashboard.

## Architecture

Caller
→ Vapi
→ FastAPI
→ PostgreSQL
→ Dashboard

## Current Features

- Patient registration API
- PostgreSQL persistence
- SQLAlchemy ORM
- Pydantic validation
- Patient CRUD operations
- Soft deletion
- Search/filter patients
- Centralized API error handling
- Automated pytest tests
- Simple HTML/JavaScript dashboard

## Patient Registration Data

Required:

- First name
- Last name
- Date of birth
- Sex
- US phone number
- Address
- City
- State
- ZIP code

Optional:

- Email
- Insurance provider
- Insurance member ID
- Preferred language
- Emergency contact

## API Endpoints

### Health

GET `/health`

### List Patients

GET `/patients`

Optional filters:

- `last_name`
- `date_of_birth`
- `phone_number`

### Get Patient

GET `/patients/{patient_id}`

### Create Patient

POST `/patients`

### Update Patient

PUT `/patients/{patient_id}`

### Delete Patient

DELETE `/patients/{patient_id}`

Deletion is implemented as a soft delete.

## Running Locally

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1