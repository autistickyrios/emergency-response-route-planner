from fastapi import APIRouter, HTTPException

from backend.app.models.incident import (
    Incident,
    IncidentCreate,
    IncidentStatus,
)
from backend.app.services.incident_service import (
    incident_service,
)


router = APIRouter(
    prefix="/api/incidents",
    tags=["Incidents"],
)


@router.post(
    "",
    response_model=Incident,
)
def create_incident(
    request: IncidentCreate,
):

    return incident_service.create_incident(request)


@router.get(
    "/active",
    response_model=list[Incident],
)
def get_active_incidents():

    return incident_service.get_active_incidents()


@router.get(
    "/{incident_id}",
    response_model=Incident,
)
def get_incident(
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

    return incident


@router.patch(
    "/{incident_id}/status",
    response_model=Incident,
)
def update_incident_status(
    incident_id: str,
    status: IncidentStatus,
):

    if status not in {
        "active",
        "dispatched",
        "resolved",
    }:
        raise HTTPException(
            status_code=400,
            detail="Invalid incident status.",
        )

    incident = incident_service.update_status(
        incident_id,
        status,
    )

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found.",
        )

    return incident