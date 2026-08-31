from fastapi import APIRouter, HTTPException

from backend.app.models.hospital import Hospital
from backend.app.services.hospital_service import (
    hospital_service,
)


router = APIRouter(
    prefix="/api/hospitals",
    tags=["Hospitals"],
)


@router.get(
    "",
    response_model=list[Hospital],
)
def get_hospitals():

    return list(
        hospital_service.hospitals.values()
    )


@router.get(
    "/operational",
    response_model=list[Hospital],
)
def get_operational_hospitals():

    return (
        hospital_service
        .get_operational_hospitals()
    )


@router.get(
    "/{hospital_id}",
    response_model=Hospital,
)
def get_hospital(
    hospital_id: str,
):

    hospital = hospital_service.get_hospital(
        hospital_id
    )

    if hospital is None:
        raise HTTPException(
            status_code=404,
            detail="Hospital not found.",
        )

    return hospital