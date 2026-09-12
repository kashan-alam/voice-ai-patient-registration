# Voice AI Patient Registration System

A voice-based patient registration system that allows callers to provide their registration information through a natural voice conversation.

The system uses **Vapi** for voice interaction, speech-to-text, text-to-speech, LLM-based conversation handling, and tool calling. **FastAPI** provides the backend API, validation, and business logic, while **PostgreSQL** stores patient information.

---

## Overview

The system allows a patient to register through a voice conversation with an AI assistant.

The AI agent:

1. Greets the caller.
2. Collects required patient information.
3. Collects optional information when available.
4. Understands natural spoken responses.
5. Handles information provided out of order.
6. Handles corrections to previously provided information.
7. Reads the complete registration back to the caller.
8. Requires explicit confirmation before saving.
9. Sends the confirmed information to the backend.
10. Validates the information again on the backend.
11. Stores the patient in PostgreSQL.
12. Confirms successful registration to the caller.

The application also provides a REST API and a simple web dashboard for viewing and managing registered patients.

---

## Architecture

```text
                         Caller
                    Phone / Browser
                           |
                           v
                    +-------------+
                    |    Vapi     |
                    |-------------|
                    | Voice / STT |
                    | TTS         |
                    | LLM         |
                    | Tool Calling|
                    +------+------+
                           |
                    create_patient
                           |
                           v
                    +-------------+
                    |   FastAPI   |
                    |-------------|
                    | REST API    |
                    | Validation  |
                    | Business    |
                    | Logic       |
                    +------+------+
                           |
                           v
                    +-------------+
                    | PostgreSQL  |
                    |-------------|
                    |  Patients   |
                    +------+------+
                           ^
                           |
                    +------+------+
                    |  Dashboard  |
                    | HTML + JS   |
                    +-------------+
```

### Registration Flow

```text
Caller
  |
  v
Collect information
  |
  v
Validate information
  |
  v
Handle corrections
  |
  v
Read complete record back
  |
  v
Explicit caller confirmation
  |
  v
create_patient tool
  |
  v
FastAPI
  |
  v
Backend validation
  |
  v
PostgreSQL
  |
  v
Success response
  |
  v
Tell caller registration is complete
```

> The system does not intentionally save a patient before explicit confirmation.

---

## Technology Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL
- pytest

### Voice AI

- Vapi
- OpenAI model through Vapi
- Vapi speech-to-text
- Vapi text-to-speech

### Frontend

- HTML
- CSS
- JavaScript

### Deployment

- Railway
- Railway PostgreSQL

### Development

- Git
- GitHub
- VS Code

---

## Main Features

### Voice Patient Registration

Patients can provide their information naturally through speech.

For example:

- "My name is John Davis."
- "I was born January fifth, nineteen ninety-five."
- "My phone number is four one five five five five one two three four."
- "I live at 123 Market Street in San Francisco, California."

The agent can also process multiple pieces of information provided in a single response.

### Patient Information

#### Required Fields

- First name
- Last name
- Date of birth
- Sex
- Phone number
- Address line 1
- City
- State
- ZIP code

#### Optional Fields

- Address line 2
- Email
- Insurance provider
- Insurance member ID
- Preferred language
- Emergency contact name
- Emergency contact phone

#### Automatically Generated Fields

- Patient ID (UUID)
- Created timestamp
- Updated timestamp
- Deleted timestamp

---

## Data Validation

Validation is performed on the backend using Pydantic schemas and custom validation functions.

Backend validation is important because the LLM should not be the only layer responsible for determining whether patient information is valid.

### Names

Names must contain valid alphabetic characters and may contain:

- Spaces
- Hyphens
- Apostrophes

Examples:

- John
- Mary Jane
- Smith-Jones
- O'Connor

### Phone Numbers

US phone numbers are normalized to a 10-digit representation.

Examples:

- 415-555-1234
- (415) 555-1234
- +1 415 555 1234

### Date of Birth

The date must be valid and cannot be in the future.

### State

The state must be a valid US state abbreviation.

Examples:

- CA
- NY
- TX
- FL

The voice agent can understand full state names and provide the normalized abbreviation to the backend.

### ZIP Code

Supported formats:

- 94105
- 94105-1234

### Email

If provided, the email address must have a valid email format.

### Insurance Member ID

Insurance member IDs are validated for supported alphanumeric characters, hyphens, and underscores.

---

## Correction Handling

The system maintains the current patient information during the conversation.

If the caller corrects previously provided information, the new value replaces the old value.

**Example:**

> **Agent:** What is your last name?
>
> **Caller:** Davies.
>
> **Agent:** Thank you. What is your date of birth?
>
> **Caller:** Actually, my last name is Davis, not Davies.

The current state becomes:

```text
last_name = "Davis"
```

The previous value "Davies" is not retained as the patient's current last name.

The same behavior applies to other fields.

**Example:**

> **Caller:** My ZIP code is 94107, not 94105.

The current value becomes:

```text
zip_code = "94107"
```

---

## Out-of-Order Information

The caller does not have to provide information in exactly the order requested by the agent.

For example, if the agent asks for the date of birth and the caller responds with:

> "My name is John Davis and I live at 123 Market Street."

the agent can retain the useful information and continue collecting the missing information.

---

## Multiple Fields in One Response

The agent can process multiple pieces of information when the caller provides them together.

For example:

> "My name is John Davis, I was born January 5th 1995, and I live in San Francisco."

The information can be retained and the agent can continue with the remaining missing fields.

---

## Optional Information

Optional information does not block registration.

If the caller refuses to provide an optional field, the agent respects the decision and continues.

**Example:**

> **Agent:** What is your email address?
>
> **Caller:** I don't want to provide one.
>
> **Agent:** That's okay.

The optional field remains empty.

---

## Start Over

If the caller asks to start over, the unconfirmed patient information can be cleared and the registration process can begin again.

This prevents information from an abandoned registration attempt from being unintentionally saved.

---

## Confirmation Before Saving

Confirmation is one of the most important parts of the system.

The agent must not save the patient immediately after collecting the information.

The required flow is:

```text
Collect information
        |
        v
Validate information
        |
        v
Allow corrections
        |
        v
Read complete record back
        |
        v
Ask for explicit confirmation
        |
        v
Caller confirms
        |
        v
create_patient
        |
        v
FastAPI validation
        |
        v
PostgreSQL
```

Examples of explicit confirmation include:

- "Yes."
- "Yes, that's correct."
- "Everything is correct."
- "Yes, save it."

Silence, hesitation, or unrelated speech should not be treated as confirmation.

### Corrections During Confirmation

If the caller corrects information while the final record is being confirmed, the system does not save immediately.

**Example:**

> **Agent:** Your ZIP code is 94105. Is everything correct?
>
> **Caller:** No, the ZIP code is 94107.

The agent must:

1. Update the ZIP code.
2. Avoid calling `create_patient`.
3. Read the corrected information back.
4. Ask for confirmation again.
5. Save only after explicit confirmation.

---

## Vapi Integration

The system uses a dedicated Vapi assistant:

**Patient Registration Agent**

The assistant uses a custom function:

**`create_patient`**

The function sends the confirmed patient information to the FastAPI backend.

### Vapi-to-Backend Flow

```text
Vapi
  |
  | create_patient
  v
POST /vapi/tools/create-patient
  |
  v
FastAPI
  |
  v
Pydantic Validation
  |
  v
Patient Service
  |
  v
PostgreSQL
```

The Vapi tool endpoint is protected using a shared secret passed through:

```
X-Vapi-Tool-Secret
```

The backend validates this secret before processing the tool request.

---

## REST API

### List Patients

```http
GET /patients
```

Optional filters:

- `last_name`
- `date_of_birth`
- `phone_number`

Example:

```http
GET /patients?last_name=Davis
```

Soft-deleted patients are excluded by default.

### Get Patient

```http
GET /patients/{patient_id}
```

Returns a single active patient.

### Create Patient

```http
POST /patients
```

Returns:

```
201 Created
```

The backend validates the patient information before saving it.

### Update Patient

```http
PUT /patients/{patient_id}
```

Partial updates are supported.

The `updated_at` timestamp is changed when a patient is updated.

The original `created_at` timestamp remains unchanged.

### Delete Patient

```http
DELETE /patients/{patient_id}
```

Deletion uses soft delete.

The database record is retained and `deleted_at` is populated.

Deleted patients are excluded from normal patient queries.

### Vapi Tool Endpoint

```http
POST /vapi/tools/create-patient
```

This endpoint receives Vapi custom tool requests and creates the patient after backend validation.

### API Response Format

Successful responses use:

```json
{
  "data": {},
  "error": null
}
```

Errors use:

```json
{
  "data": null,
  "error": {
    "message": "Patient not found"
  }
}
```

### HTTP Status Codes

| Status Code | Meaning                     |
|-------------|------------------------------|
| 200         | Successful request           |
| 201         | Patient successfully created |
| 400         | Invalid request              |
| 401         | Unauthorized Vapi tool request |
| 404         | Patient not found            |
| 422         | Validation error             |
| 500         | Unexpected server error      |

---

## Dashboard

The project includes a simple HTML/CSS/JavaScript dashboard.

The dashboard allows users to:

- View registered patients
- Filter patients
- Search by last name
- Search by date of birth
- Search by phone number
- View patient information
- Soft-delete patients
- Clear filters

No frontend framework is required.

---

## Database

PostgreSQL is used for persistent storage.

The main table is:

**`patients`**

Important fields include:

- `patient_id`
- `first_name`
- `last_name`
- `date_of_birth`
- `sex`
- `phone_number`
- `address_line_1`
- `address_line_2`
- `city`
- `state`
- `zip_code`
- `email`
- `insurance_provider`
- `insurance_member_id`
- `preferred_language`
- `emergency_contact_name`
- `emergency_contact_phone`
- `created_at`
- `updated_at`
- `deleted_at`

Indexes are included for commonly queried fields such as:

- Last name
- Date of birth
- Phone number

---

## Project Structure

```text
voice-ai-patient-registration/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── patients.py
│   │   └── vapi.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── exceptions.py
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── models.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── patient.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── patient_service.py
│   │
│   └── utils/
│       ├── __init__.py
│       └── validation.py
│
├── dashboard/
│   ├── index.html
│   └── app.js
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_patients.py
│
├── .env.example
├── .gitignore
├── Procfile
├── requirements.txt
└── README.md
```

---

## Environment Variables

Create a `.env` file for local development.

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/voice_ai_patient_registration
TEST_DATABASE_URL=postgresql://username:password@localhost:5432/voice_ai_patient_registration_test
VAPI_API_KEY=your_vapi_api_key
VAPI_TOOL_SECRET=your_vapi_tool_secret
APP_NAME=Voice AI Patient Registration System
APP_ENV=development
```

---

## Security

The real `.env` file must never be committed to GitHub.

The repository contains `.env.example` instead.

---

## Local Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd voice-ai-patient-registration
```

### 2. Create a Virtual Environment

Windows PowerShell:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file and configure the required database and Vapi settings.

### 5. Start the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Swagger documentation:

```
http://127.0.0.1:8000/docs
```

Dashboard:

```
http://127.0.0.1:8000/dashboard
```

---

## Running Tests

The project uses a separate PostgreSQL database for automated tests.

Run:

```bash
pytest -v
```

The test suite covers important patient API functionality including:

- Patient creation
- Patient retrieval
- Patient listing
- Filtering
- Patient updates
- Soft deletion
- Validation
- Error handling

The Vapi tool endpoint can also be tested independently by sending a Vapi-style tool request to:

```http
POST /vapi/tools/create-patient
```

This allows the backend integration to be tested without making a paid phone call.

---

## Deployment

The backend is deployed using Railway.

Production architecture:

```text
Vapi
  |
  v
Railway FastAPI Application
  |
  v
Railway PostgreSQL
```

Production environment variables are configured through Railway rather than committed to the repository.

---

## Vapi Configuration

The voice assistant is configured as:

**Patient Registration Agent**

The assistant uses:

- Voice interaction
- Speech-to-text
- Text-to-speech
- OpenAI-powered conversation through Vapi
- Patient registration instructions
- `create_patient` custom tool

The custom tool communicates with:

```http
POST /vapi/tools/create-patient
```

The assistant is configured to call the tool only after:

1. Required information has been collected.
2. Information has been validated.
3. The complete record has been read back.
4. The caller has explicitly confirmed the information.

---

## Example Conversation

> **Agent:** Thank you for calling our patient registration line. My name is Alex. I can help you register as a patient. What is your first name?
>
> **Caller:** John.
>
> **Agent:** And your last name?
>
> **Caller:** Davis.
>
> **Agent:** What is your date of birth?
>
> **Caller:** January 5th, 1995.
>
> **Agent:** What is your sex?
>
> **Caller:** Male.
>
> **Agent:** What is your phone number?
>
> **Caller:** 415-555-1234.
>
> **Agent:** What is your street address?
>
> **Caller:** 123 Market Street.
>
> **Agent:** What city and state do you live in?
>
> **Caller:** San Francisco, California.
>
> **Agent:** What is your ZIP code?
>
> **Caller:** 94105.
>
> *...*
>
> **Agent:** Let me read everything back to you.
>
> *[Complete patient information]*
>
> Is everything correct?
>
> **Caller:** Yes, that's correct.
>
> **Agent:** Thank you. Your registration has been successfully completed.

---

## Edge Cases

The system is designed to handle:

- Invalid phone numbers
- Invalid ZIP codes
- Invalid states
- Future dates of birth
- Invalid email addresses
- Missing required information
- Corrections during data collection
- Corrections during final confirmation
- Multiple fields provided in one response
- Information provided out of order
- Optional information refusal
- Requests to start over
- Ambiguous confirmation
- Backend validation failure
- Database errors
- Unauthorized Vapi tool requests
- Soft-deleted patients
- Invalid patient IDs

---

## Error Handling

Backend errors are handled without exposing internal stack traces to callers.

Unexpected server errors return:

```json
{
  "data": null,
  "error": {
    "message": "An unexpected server error occurred."
  }
}
```

Database transactions are rolled back when a patient creation or update fails.

The system does not claim that a registration was successfully completed unless the backend confirms that the database operation succeeded.

---

## Security Considerations

The project uses:

- Environment variables for secrets
- `.gitignore` protection for `.env`
- Vapi tool authentication
- Backend-side validation
- SQLAlchemy ORM/database operations
- Controlled API error messages
- Soft deletion

No real patient information should be used during testing or demonstration.

Only synthetic/fake patient data should be used for this assessment.

---

## Voice Testing

The Vapi voice flow can be tested through Vapi's browser calling functionality.

The backend and Vapi tool integration can also be tested independently without a physical phone call.

The backend verification confirms the following flow:

```text
Vapi-style tool request
        |
        v
FastAPI
        |
        v
Pydantic validation
        |
        v
Patient service
        |
        v
PostgreSQL
```

A physical US phone call may require appropriate telephony access and can incur calling charges depending on the caller's carrier and location.

---

## Limitations

This project is designed as a technical assessment/demo and therefore does not implement every requirement that would be necessary for a production healthcare system.

Examples of current limitations include:

- Browser/telephony testing depends on Vapi availability and network conditions.
- No advanced call recovery/resume mechanism is implemented.
- Idempotency protection for repeated tool calls could be added for production.
- Production-grade authentication and authorization for the dashboard are not implemented.
- Advanced audit logging is not implemented.

---

## HIPAA / Production Disclaimer

This project is a technical assessment/demo application and is not intended to be considered a production HIPAA-compliant healthcare system.

A production healthcare deployment would require additional technical, organizational, and legal controls, potentially including:

- Appropriate access control
- Role-based authorization
- Audit logging
- Encryption
- Secure data retention policies
- Monitoring and alerting
- Appropriate vendor agreements
- HIPAA-compliant infrastructure and services
- Security and compliance review
- Production-grade data protection

No real patient or protected health information (PHI) should be used with this demonstration system.

---

## Future Improvements

Potential improvements for a production version include:

- Strong authentication and authorization
- Role-based dashboard access
- Audit logging
- Idempotency protection for repeated Vapi tool calls
- More comprehensive automated tests
- Better observability and monitoring
- Production-grade telephony configuration
- Call recovery and resume support
- Encrypted sensitive data handling
- HIPAA-compliant infrastructure and vendor agreements
- Advanced security and compliance controls