from typing import Literal

from pydantic import BaseModel


AmbulanceStatus = Literal[
    "available",
    "dispatched",
    "busy",
    "offline",
]


class Ambulance(BaseModel):
    id: str
    name: str
    location: str
    status: AmbulanceStatus = "available"
    medical_support: bool = True
    crew_level: Literal["basic", "advanced"] = "basic"