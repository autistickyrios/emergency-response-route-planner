from fastapi import APIRouter, HTTPException

from backend.app.models.route import (
    RouteRequest,
    RouteResponse,
)
from backend.app.services.graph_service import CITY_GRAPH
from backend.app.services.routing_service import (
    calculate_route,
    calculate_route_metrics,
)

router = APIRouter(
    prefix="/api/routes",
    tags=["Routing"],
)


@router.post("/calculate", response_model=RouteResponse)
def calculate(request: RouteRequest):

    try:
        path = calculate_route(
            CITY_GRAPH,
            request.source,
            request.destination,
            request.algorithm,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    if path is None:
        raise HTTPException(
            status_code=404,
            detail="No route found.",
        )

    distance, travel_time = calculate_route_metrics(
        CITY_GRAPH,
        path,
    )

    return RouteResponse(
        algorithm=request.algorithm,
        path=path,
        total_distance_km=round(distance, 2),
        estimated_time_minutes=round(travel_time, 2),
        nodes_explored=len(path),
    )