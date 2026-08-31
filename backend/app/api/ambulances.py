from fastapi import APIRouter, HTTPException

from backend.app.models.ambulance import Ambulance
from backend.app.services.ambulance_service import (
    ambulance_service,
)


router = APIRouter(
    prefix="/api/ambulances",
    tags=["Ambulances"],
)


@router.get(
    "",
    response_model=list[Ambulance],
)
def get_ambulances():

    return list(
        ambulance_service.ambulances.values()
    )


@router.get(
    "/available",
    response_model=list[Ambulance],
)
def get_available_ambulances():

    return ambulance_service.get_available_ambulances()


@router.get(
    "/{ambulance_id}",
    response_model=Ambulance,
)
def get_ambulance(
    ambulance_id: str,
):

    ambulance = ambulance_service.get_ambulance(
        ambulance_id
    )

    if ambulance is None:
        raise HTTPException(
            status_code=404,
            detail="Ambulance not found.",
        )

    return ambulance