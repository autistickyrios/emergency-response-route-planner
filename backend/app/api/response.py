from fastapi import APIRouter, HTTPException

from backend.app.services.incident_service import (
    incident_service,
)
from backend.app.services.response_service import (
    create_response_plan,
)


router = APIRouter(
    prefix="/api/response",
    tags=["Emergency Response"],
)


@router.post("/{incident_id}")
def generate_response_plan(
    incident_id: str,
):

    incident = incident_service.get_incident(
        incident_id
    )

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found.",
        )

    try:
        result = create_response_plan(
            incident_id
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    if result is None:
        raise HTTPException(
            status_code=409,
            detail=(
                "Unable to create a complete "
                "emergency response plan."
            ),
        )

    return result