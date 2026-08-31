from typing import Dict

from backend.app.models.hospital import Hospital


class HospitalService:

    def __init__(self):
        self.hospitals: Dict[str, Hospital] = {}

    def add_hospital(
        self,
        hospital: Hospital,
    ) -> Hospital:

        self.hospitals[hospital.id] = hospital
        return hospital

    def get_hospital(
        self,
        hospital_id: str,
    ) -> Hospital | None:

        return self.hospitals.get(hospital_id)

    def get_operational_hospitals(
        self,
    ) -> list[Hospital]:

        return [
            hospital
            for hospital in self.hospitals.values()
            if hospital.status != "closed"
            and hospital.emergency_department
        ]


hospital_service = HospitalService()


def initialize_demo_hospitals():

    demo_hospitals = [
        Hospital(
            id="HOS-001",
            name="Central General Hospital",
            location="hospital_01",
            status="operational",
            emergency_capacity=20,
            icu_beds_available=8,
            trauma_center=True,
            emergency_department=True,
        ),
        Hospital(
            id="HOS-002",
            name="East City Hospital",
            location="hospital_02",
            status="operational",
            emergency_capacity=12,
            icu_beds_available=4,
            trauma_center=False,
            emergency_department=True,
        ),
        Hospital(
            id="HOS-003",
            name="West Trauma Center",
            location="hospital_03",
            status="busy",
            emergency_capacity=5,
            icu_beds_available=1,
            trauma_center=True,
            emergency_department=True,
        ),
        Hospital(
            id="HOS-004",
            name="South Medical Center",
            location="hospital_04",
            status="closed",
            emergency_capacity=15,
            icu_beds_available=6,
            trauma_center=True,
            emergency_department=True,
        ),
    ]

    for hospital in demo_hospitals:
        hospital_service.add_hospital(hospital)


initialize_demo_hospitals()