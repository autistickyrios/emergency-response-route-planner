from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.services.ambulance_service import (
    ambulance_service,
)
from backend.app.services.incident_service import (
    incident_service,
)


client = TestClient(app)


def reset_state():

    ambulance_service.ambulances.clear()

    incident_service.incidents.clear()
    incident_service._next_id = 1

    from backend.app.services.ambulance_service import (
        initialize_demo_fleet,
    )

    initialize_demo_fleet()


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_get_ambulances():

    reset_state()

    response = client.get(
        "/api/ambulances"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 4


def test_create_incident():

    reset_state()

    response = client.post(
        "/api/incidents",
        json={
            "emergency_type": "medical",
            "severity": "critical",
            "location": "junction_02",
            "description": "Test emergency",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == "INC-001"
    assert data["status"] == "active"


def test_dispatch_incident():

    reset_state()

    create_response = client.post(
        "/api/incidents",
        json={
            "emergency_type": "medical",
            "severity": "critical",
            "location": "junction_02",
            "description": "Cardiac emergency",
        },
    )

    assert create_response.status_code == 200

    incident_id = create_response.json()["id"]

    dispatch_response = client.post(
        f"/api/dispatch/{incident_id}"
    )

    assert dispatch_response.status_code == 200

    data = dispatch_response.json()

    assert data["incident_id"] == incident_id
    assert data["ambulance_id"].startswith("AMB-")
    assert data["status"] == "dispatched"

    incident = incident_service.get_incident(
        incident_id
    )

    assert incident.status == "dispatched"


def test_dispatch_nonexistent_incident():

    reset_state()

    response = client.post(
        "/api/dispatch/INC-999"
    )

    assert response.status_code == 404