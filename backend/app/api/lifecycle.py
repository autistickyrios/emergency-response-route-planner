from fastapi import APIRouter, HTTPException

from backend.app.services.ambulance_service import (
    ambulance_service,
)
from backend.app.services.incident_service import (
    incident_service,
)


router = APIRouter(
    prefix="/api/incidents",
    tags=["Incident Lifecycle"],
)


def get_incident_or_404(
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


@router.post("/{incident_id}/arrive")
def ambulance_arrived(
    incident_id: str,
):

    incident = get_incident_or_404(
        incident_id
    )

    if incident.status != "dispatched":
        raise HTTPException(
            status_code=409,
            detail=(
                "Incident must be dispatched "
                "before ambulance arrival."
            ),
        )

    incident_service.update_status(
        incident_id,
        "at_scene",
    )

    return {
        "incident_id": incident_id,
        "status": "at_scene",
        "message": "Ambulance has arrived at the scene.",
    }


@router.post("/{incident_id}/transport")
def begin_transport(
    incident_id: str,
):

    incident = get_incident_or_404(
        incident_id
    )

    if incident.status != "at_scene":
        raise HTTPException(
            status_code=409,
            detail=(
                "Incident must be at the scene "
                "before transport begins."
            ),
        )

    incident_service.update_status(
        incident_id,
        "transporting",
    )

    return {
        "incident_id": incident_id,
        "status": "transporting",
        "message": "Patient transport has started.",
    }


@router.post("/{incident_id}/resolve")
def resolve_incident(
    incident_id: str,
):

    incident = get_incident_or_404(
        incident_id
    )

    if incident.status != "transporting":
        raise HTTPException(
            status_code=409,
            detail=(
                "Incident must be transporting "
                "before it can be resolved."
            ),
        )

    incident_service.update_status(
        incident_id,
        "resolved",
    )

    return {
        "incident_id": incident_id,
        "status": "resolved",
        "message": "Emergency response completed.",
    }