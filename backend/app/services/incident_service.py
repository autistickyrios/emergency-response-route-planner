from typing import Dict

from backend.app.models.incident import (
    Incident,
    IncidentCreate,
)


class IncidentService:

    def __init__(self):
        self.incidents: Dict[str, Incident] = {}
        self._next_id = 1

    def create_incident(
        self,
        incident_data: IncidentCreate,
    ) -> Incident:

        incident_id = f"INC-{self._next_id:03d}"
        self._next_id += 1

        incident = Incident(
            id=incident_id,
            emergency_type=incident_data.emergency_type,
            severity=incident_data.severity,
            location=incident_data.location,
            description=incident_data.description,
        )

        self.incidents[incident_id] = incident

        return incident

    def get_incident(
        self,
        incident_id: str,
    ) -> Incident | None:

        return self.incidents.get(incident_id)

    def get_active_incidents(self) -> list[Incident]:

        return [
            incident
            for incident in self.incidents.values()
            if incident.status == "active"
        ]

    def update_status(
        self,
        incident_id: str,
        status: str,
    ) -> Incident | None:

        incident = self.incidents.get(incident_id)

        if incident is None:
            return None

        incident.status = status

        return incident


incident_service = IncidentService()