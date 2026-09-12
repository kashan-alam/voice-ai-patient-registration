import secrets

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.database import get_db
from app.schemas.patient import PatientCreate
from app.services.patient_service import create_patient


router = APIRouter(
    prefix="/vapi",
    tags=["Vapi"],
)


@router.post("/tools/create-patient")
def vapi_create_patient(
    payload: dict,
    db: Session = Depends(get_db),
    x_vapi_tool_secret: str | None = Header(default=None),
):
    """
    Receive a Vapi create_patient function call.

    Vapi calls this endpoint only after the voice assistant
    has collected and confirmed the patient's information.
    """

    # ---------------------------------------------------------
    # 1. Verify the shared secret
    # ---------------------------------------------------------

    if not settings.vapi_tool_secret:
        raise HTTPException(
            status_code=500,
            detail="Vapi tool secret is not configured.",
        )

    if not x_vapi_tool_secret or not secrets.compare_digest(
        x_vapi_tool_secret,
        settings.vapi_tool_secret,
    ):
        raise HTTPException(
            status_code=401,
            detail="Unauthorized.",
        )

    # ---------------------------------------------------------
    # 2. Verify the Vapi message structure
    # ---------------------------------------------------------

    message = payload.get("message", {})

    if message.get("type") != "tool-calls":
        raise HTTPException(
            status_code=400,
            detail="Invalid Vapi tool call.",
        )

    tool_calls = message.get("toolCallList", [])

    if not tool_calls:
        raise HTTPException(
            status_code=400,
            detail="No tool call was provided.",
        )

    results = []

    # ---------------------------------------------------------
    # 3. Process tool calls
    # ---------------------------------------------------------

    for tool_call in tool_calls:

        tool_call_id = tool_call.get("id")
        function_name = tool_call.get("name")

        # Current Vapi payload uses "parameters".
        # Some payload formats can expose arguments under
        # function.arguments, so we support both.
        parameters = tool_call.get("parameters")

        if parameters is None:
            function_data = tool_call.get("function", {})
            parameters = function_data.get("arguments", {})

        if not isinstance(parameters, dict):
            results.append(
                {
                    "toolCallId": tool_call_id,
                    "result": "Invalid patient data was provided.",
                }
            )
            continue

        # -----------------------------------------------------
        # 4. Make sure this is our expected function
        # -----------------------------------------------------

        if function_name != "create_patient":
            results.append(
                {
                    "toolCallId": tool_call_id,
                    "result": f"Unknown tool: {function_name}",
                }
            )
            continue

        # -----------------------------------------------------
        # 5. Validate patient data using our existing schema
        # -----------------------------------------------------

        try:
            patient_data = PatientCreate.model_validate(parameters)

        except Exception as exc:
            results.append(
                {
                    "toolCallId": tool_call_id,
                    "result": (
                        "Patient information failed backend validation. "
                        "Please correct the information and try again."
                    ),
                }
            )
            continue

        # -----------------------------------------------------
        # 6. Save patient using existing service
        # -----------------------------------------------------

        try:
            patient = create_patient(
                db=db,
                patient_data=patient_data,
            )

            results.append(
                {
                    "toolCallId": tool_call_id,
                    "result": (
                        "Patient registration was successfully saved. "
                        f"Patient ID: {patient.patient_id}"
                    ),
                }
            )

        except Exception:
            db.rollback()

            results.append(
                {
                    "toolCallId": tool_call_id,
                    "result": (
                        "The patient registration could not be saved "
                        "because of a temporary backend error."
                    ),
                }
            )

    # ---------------------------------------------------------
    # 7. Return Vapi-compatible response
    # ---------------------------------------------------------

    return {
        "results": results,
    }