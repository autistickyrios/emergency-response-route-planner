from backend.app.services.ambulance_service import (
    ambulance_service,
)
from backend.app.services.graph_service import CITY_GRAPH
from backend.app.services.incident_service import (
    incident_service,
)
from backend.app.services.routing_service import (
    calculate_route,
    calculate_route_metrics,
)


def find_best_ambulance(
    incident_id: str,
) -> dict | None:

    incident = incident_service.get_incident(
        incident_id
    )

    if incident is None:
        raise ValueError("Incident not found.")

    available_ambulances = (
        ambulance_service
        .get_available_ambulances()
    )

    if not available_ambulances:
        return None

    candidates = []

    for ambulance in available_ambulances:

        try:
            path = calculate_route(
                CITY_GRAPH,
                ambulance.location,
                incident.location,
                "astar",
            )

        except ValueError:
            continue

        if path is None:
            continue

        distance, travel_time = (
            calculate_route_metrics(
                CITY_GRAPH,
                path,
            )
        )

        candidates.append(
            {
                "ambulance": ambulance,
                "path": path,
                "distance": distance,
                "travel_time": travel_time,
            }
        )

    if not candidates:
        return None

    candidates.sort(
        key=lambda candidate:
        candidate["travel_time"]
    )

    return candidates[0]