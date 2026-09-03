# Emergency Response Route Planner

An intelligent emergency response coordination system that selects suitable ambulances, calculates optimized routes using A* graph search, recommends hospitals, and manages the complete emergency response lifecycle.

[Live Demo](https://emergency-response-route-planner.vercel.app) · [API Documentation](https://emergency-response-route-planner.onrender.com/docs)

> Academic project using a simulated road network and emergency-response dataset.

## Overview

Emergency response teams need to make several decisions quickly:

- Which ambulance should respond?
- What is the fastest available route?
- Which hospital should receive the patient?
- How should the response be tracked from dispatch to resolution?

This project models that workflow as a centralized emergency operations control center.

## Features

### Incident Management

Create incidents with:

- Emergency type
- Severity
- Location
- Call notes

### Ambulance Dispatch

The system evaluates available ambulances and selects the unit with the lowest estimated response time.

### A* Route Optimization

Routes are calculated using A* search over a weighted graph representing a simulated road network.

### Hospital Selection

The system evaluates available hospitals and generates a route from the incident location to the selected facility.

### Response Lifecycle

```text
Incident Created
       ↓
Response Plan Generated
       ↓
Ambulance Dispatched
       ↓
Ambulance Arrives
       ↓
Patient Transport
       ↓
Incident Resolved
       ↓
Ambulance Available
```

### Fleet Monitoring

The dashboard provides operational visibility into:

- Available units
- En-route units
- Units on assignment
- Offline units
- Ambulance capability
- Medical support level

## Architecture

```text
                    React + Vite
                         │
                         │ REST API
                         ▼
                     FastAPI
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
      Incident       Dispatch       Hospital
      Service         Service        Selection
                         │
                         ▼
                    A* Routing
                         │
                         ▼
                  Weighted Graph
```

## Routing Algorithm

The routing engine represents the emergency response area as a weighted graph.

Each edge contains simulated distance and travel-time information.

For an ambulance and incident:

1. Find all available ambulances.
2. Calculate an A* route from each ambulance to the incident.
3. Compare estimated travel times.
4. Select the fastest suitable ambulance.
5. Calculate the route to the selected hospital.
6. Return the complete response plan.

A* evaluates routes using:

```text
f(n) = g(n) + h(n)
```

where:

- `g(n)` is the cost from the starting node.
- `h(n)` is the estimated cost to the destination.
- `f(n)` is the estimated total route cost.

## Tech Stack

| Layer | Technologies |
|---|---|
| Frontend | React, Vite, Axios |
| Backend | Python, FastAPI, Pydantic |
| Algorithms | A* Search, Graph Traversal |
| UI | CSS, Lucide Icons |
| Deployment | Vercel, Render |

## Project Structure

```text
emergency-response-route-planner/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   └── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   └── package.json
│
└── README.md
```

## API

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/ambulances` | Get ambulance fleet |
| GET | `/api/ambulances/available` | Get available ambulances |
| GET | `/api/hospitals` | Get hospitals |
| POST | `/api/incidents` | Create an incident |
| POST | `/api/response/{incident_id}` | Generate response plan |
| POST | `/api/dispatch/{incident_id}` | Dispatch ambulance |
| POST | `/api/incidents/{incident_id}/arrive` | Mark arrival |
| POST | `/api/incidents/{incident_id}/transport` | Begin transport |
| POST | `/api/incidents/{incident_id}/resolve` | Resolve incident |

## Local Development

### Backend

```bash
cd backend

python -m venv .venv
source .venv/Scripts/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

### Frontend

```bash
cd frontend

npm install
npm run dev
```

## Example Incident

```json
{
  "emergency_type": "accident",
  "severity": "critical",
  "location": "junction_05",
  "description": "Major road accident"
}
```

The system then evaluates available resources, calculates routes, selects an ambulance and hospital, and manages the response lifecycle.

## Deployment

The application is deployed as two services:

```text
Vercel
  │
  │ HTTPS
  ▼
React Frontend
  │
  │ REST API
  ▼
Render
  │
  ▼
FastAPI Backend
```

## Limitations

This is an academic demonstration system rather than a production emergency-dispatch platform.

- Road network is simulated.
- Ambulance locations are predefined graph nodes.
- Traffic data is not real-time.
- GPS tracking is not implemented.
- Backend state is currently stored in memory.
- Data resets when the backend restarts or redeploys.
- Hospital data is limited for demonstration.
- Intelligence is currently based on A* search and rule/heuristic-based selection rather than a trained machine-learning model.

## Future Scope

- Real road-network integration
- Live GPS tracking
- Real-time traffic data
- Persistent database
- Multiple hospitals
- Hospital capacity and bed availability
- Dynamic ambulance positioning
- Real-time WebSocket updates
- ML-based ETA prediction
- Historical incident analytics
- Authentication and role-based access

## Project Context

Developed as an academic project demonstrating the application of AI concepts, graph search, resource allocation, REST API development, and full-stack software engineering.

## Author

**Hitesh / LEVENINE**

Bachelor of Vocation — Software Development

GitHub: [@autistickyrios](https://github.com/autistickyrios)

## License

This project is intended for educational and demonstration purposes.
