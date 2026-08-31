from backend.app.services.dispatch_service import (
    find_best_ambulance,
)
from backend.app.services.hospital_selection_service import (
    find_best_hospital,
)
from backend.app.services.incident_service import (
    incident_service,
)


def create_response_plan(
    incident_id: str,
) -> dict | None:

    incident = incident_service.get_incident(
        incident_id
    )

    if incident is None:
        raise ValueError("Incident not found.")

    ambulance_result = find_best_ambulance(
        incident_id
    )

    if ambulance_result is None:
        return None

    hospital_result = find_best_hospital(
        incident.location,
        incident.emergency_type,
    )

    if hospital_result is None:
        return None

    ambulance = ambulance_result["ambulance"]
    hospital = hospital_result["hospital"]

    incident_service.assign_ambulance(
    incident_id,
    ambulance.id,
    )

    total_distance = (
        ambulance_result["distance"]
        + hospital_result["distance"]
    )

    total_time = (
        ambulance_result["travel_time"]
        + hospital_result["travel_time"]
    )

    return {
        "incident": {
            "id": incident.id,
            "type": incident.emergency_type,
            "severity": incident.severity,
            "location": incident.location,
            "status": incident.status,
        },
        "ambulance": {
            "id": ambulance.id,
            "name": ambulance.name,
            "location": ambulance.location,
        },
        "route_to_incident": {
            "path": ambulance_result["path"],
            "distance_km": round(
                ambulance_result["distance"],
                2,
            ),
            "estimated_time_minutes": round(
                ambulance_result["travel_time"],
                2,
            ),
        },
        "hospital": {
            "id": hospital.id,
            "name": hospital.name,
            "location": hospital.location,
        },
        "route_to_hospital": {
            "path": hospital_result["path"],
            "distance_km": round(
                hospital_result["distance"],
                2,
            ),
            "estimated_time_minutes": round(
                hospital_result["travel_time"],
                2,
            ),
        },
        "total_distance_km": round(
            total_distance,
            2,
        ),
        "total_estimated_time_minutes": round(
            total_time,
            2,
        ),
    }