import pytest

from backend.app.services.ambulance_service import (
    ambulance_service,
)
from backend.app.services.dispatch_service import (
    find_best_ambulance,
)
from backend.app.services.incident_service import (
    incident_service,
)
from backend.app.models.incident import IncidentCreate


@pytest.fixture(autouse=True)
def reset_state():
    """
    Reset in-memory services before every test.
    """

    ambulance_service.ambulances.clear()

    incident_service.incidents.clear()
    incident_service._next_id = 1

    from backend.app.services.ambulance_service import (
        initialize_demo_fleet,
    )

    initialize_demo_fleet()

    yield


def create_test_incident(
    location="junction_02",
    severity="critical",
):
    return incident_service.create_incident(
        IncidentCreate(
            emergency_type="medical",
            severity=severity,
            location=location,
            description="Test emergency",
        )
    )


def test_find_best_ambulance():

    incident = create_test_incident()

    result = find_best_ambulance(
        incident.id
    )

    assert result is not None
    assert result["ambulance"] is not None
    assert result["path"] is not None
    assert result["travel_time"] >= 0


def test_offline_ambulance_is_ignored():

    incident = create_test_incident()

    result = find_best_ambulance(
        incident.id
    )

    assert result is not None
    assert result["ambulance"].status == "available"

    assert result["ambulance"].id != "AMB-004"


def test_missing_incident():

    with pytest.raises(ValueError):

        find_best_ambulance(
            "INC-999"
        )


def test_no_available_ambulances():

    for ambulance in ambulance_service.ambulances.values():
        ambulance.status = "offline"

    incident = create_test_incident()

    result = find_best_ambulance(
        incident.id
    )

    assert result is None