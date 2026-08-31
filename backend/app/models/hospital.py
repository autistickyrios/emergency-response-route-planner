from typing import Literal

from pydantic import BaseModel


HospitalStatus = Literal[
    "operational",
    "busy",
    "closed",
]


class Hospital(BaseModel):
    id: str
    name: str
    location: str
    status: HospitalStatus = "operational"
    emergency_capacity: int = 10
    icu_beds_available: int = 5
    trauma_center: bool = False
    emergency_department: bool = True