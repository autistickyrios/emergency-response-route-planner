from typing import Literal

from pydantic import BaseModel, Field


EmergencyType = Literal[
    "medical",
    "fire",
    "accident",
    "crime",
    "other",
]

SeverityLevel = Literal[
    "low",
    "medium",
    "high",
    "critical",
]

IncidentStatus = Literal[
    "active",
    "dispatched",
    "resolved",
]


class Incident(BaseModel):
    id: str
    emergency_type: EmergencyType
    severity: SeverityLevel
    location: str
    status: IncidentStatus = "active"
    description: str = ""


class IncidentCreate(BaseModel):
    emergency_type: EmergencyType
    severity: SeverityLevel
    location: str
    description: str = Field(
        default="",
        max_length=500,
    )