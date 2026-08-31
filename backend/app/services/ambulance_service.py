from typing import Dict

from backend.app.models.ambulance import (
    Ambulance,
    AmbulanceStatus,
)

class AmbulanceService:

    def __init__(self):
        self.ambulances: Dict[str, Ambulance] = {}

    def add_ambulance(
        self,
        ambulance: Ambulance,
    ) -> Ambulance:

        self.ambulances[ambulance.id] = ambulance
        return ambulance

    def get_ambulance(
        self,
        ambulance_id: str,
    ) -> Ambulance | None:

        return self.ambulances.get(ambulance_id)

    def get_available_ambulances(self) -> list[Ambulance]:

        return [
            ambulance
            for ambulance in self.ambulances.values()
            if ambulance.status == "available"
        ]

    def update_status(
        self,
        ambulance_id: str,
        status: AmbulanceStatus,
    ) -> Ambulance | None:

        ambulance = self.ambulances.get(ambulance_id)

        if ambulance is None:
            return None

        ambulance.status = status
        return ambulance


ambulance_service = AmbulanceService()


def initialize_demo_fleet():

    demo_ambulances = [
        Ambulance(
            id="AMB-001",
            name="Central Ambulance 01",
            location="station_01",
            status="available",
            medical_support=True,
            crew_level="advanced",
        ),
        Ambulance(
            id="AMB-002",
            name="East Ambulance 02",
            location="junction_02",
            status="available",
            medical_support=True,
            crew_level="basic",
        ),
        Ambulance(
            id="AMB-003",
            name="West Ambulance 03",
            location="junction_04",
            status="available",
            medical_support=True,
            crew_level="advanced",
        ),
        Ambulance(
            id="AMB-004",
            name="South Ambulance 04",
            location="junction_03",
            status="offline",
            medical_support=True,
            crew_level="basic",
        ),
    ]

    for ambulance in demo_ambulances:
        ambulance_service.add_ambulance(ambulance)


initialize_demo_fleet()