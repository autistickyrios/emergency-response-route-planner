from backend.app.services.graph_service import CITY_GRAPH
from backend.app.services.hospital_service import (
    hospital_service,
)
from backend.app.services.routing_service import (
    calculate_route,
    calculate_route_metrics,
)


def find_best_hospital(
    incident_location: str,
    emergency_type: str,
) -> dict | None:

    hospitals = (
        hospital_service
        .get_operational_hospitals()
    )

    if not hospitals:
        return None

    candidates = []

    for hospital in hospitals:

        path = calculate_route(
            CITY_GRAPH,
            incident_location,
            hospital.location,
            "dijkstra",
        )

        if path is None:
            continue

        distance, travel_time = (
            calculate_route_metrics(
                CITY_GRAPH,
                path,
            )
        )

        score = travel_time

        # Trauma emergencies strongly prefer
        # trauma-capable hospitals.
        if emergency_type == "accident":
            if hospital.trauma_center:
                score *= 0.7
            else:
                score *= 1.3

        # Medical emergencies benefit from
        # available ICU capacity.
        if emergency_type == "medical":
            if hospital.icu_beds_available > 0:
                score *= 0.9
            else:
                score *= 1.5

        candidates.append(
            {
                "hospital": hospital,
                "path": path,
                "distance": distance,
                "travel_time": travel_time,
                "score": score,
            }
        )

    if not candidates:
        return None

    candidates.sort(
        key=lambda candidate:
        candidate["score"]
    )

    return candidates[0]