from fastapi import APIRouter, HTTPException

from backend.app.services.ambulance_service import (
    ambulance_service,
)
from backend.app.services.dispatch_service import (
    find_best_ambulance,
)
from backend.app.services.incident_service import (
    incident_service,
)


router = APIRouter(
    prefix="/api/dispatch",
    tags=["Emergency Dispatch"],
)


@router.post("/{incident_id}")
def dispatch_incident(
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

    if incident.status != "active":
        raise HTTPException(
            status_code=400,
            detail=(
                "Incident is not available "
                "for dispatch."
            ),
        )

    result = find_best_ambulance(
        incident_id
    )

    if result is None:
        raise HTTPException(
            status_code=409,
            detail=(
                "No available ambulance "
                "can reach this incident."
            ),
        )

    ambulance = result["ambulance"]

    ambulance_service.update_status(
        ambulance.id,
        "dispatched",
    )

    incident_service.update_status(
        incident_id,
        "dispatched",
    )

    return {
        "incident_id": incident_id,
        "ambulance_id": ambulance.id,
        "ambulance_name": ambulance.name,
        "route": result["path"],
        "distance_km": round(
            result["distance"],
            2,
        ),
        "estimated_response_time_minutes": round(
            result["travel_time"],
            2,
        ),
        "status": "dispatched",
    }