# 🚑 Emergency Response Route Planner

An AI-powered emergency response routing system that helps dispatch the most suitable ambulance to an emergency, calculate efficient routes, select an appropriate hospital, and manage the complete emergency response lifecycle.

## 📌 Overview

The Emergency Response Route Planner is a full-stack application designed to assist emergency response teams in making faster and more efficient dispatch decisions.

The system takes an emergency incident as input and uses graph-based route planning and intelligent resource selection to:

- Identify the best available ambulance
- Calculate an efficient route to the incident
- Dispatch the ambulance
- Track ambulance and incident status
- Select a suitable hospital
- Calculate the route from the incident to the hospital
- Manage the incident through arrival, transport, and resolution

## ✨ Key Features

- 🚨 Emergency incident creation
- 🚑 Ambulance availability tracking
- 🧠 Automated emergency response planning
- 🗺️ A* pathfinding for route optimization
- ⚡ Intelligent ambulance selection based on estimated response time
- 🏥 Hospital selection based on emergency requirements
- 🔄 Complete incident lifecycle management
- 📊 Emergency response dashboard
- 🔌 RESTful API architecture
- 🌐 React frontend with FastAPI backend

## 🧠 How It Works

The system follows this workflow:

```text
Emergency Incident
       ↓
Create Incident
       ↓
Generate Response Plan
       ↓
Find Available Ambulances
       ↓
Calculate Routes using A*
       ↓
Select Best Ambulance
       ↓
Dispatch Ambulance
       ↓
Ambulance Arrives
       ↓
Begin Transport
       ↓
Select Suitable Hospital
       ↓
Route to Hospital
       ↓
Resolve Incident
       ↓
Ambulance Available Again
```

## 🤖 AI & Algorithms

### A* Pathfinding

The system models the emergency response network as a weighted graph.

Nodes represent locations such as:

- Ambulance stations
- Road junctions
- Hospitals

Edges represent roads and contain distance and estimated travel time.

A* search is used to find efficient routes between locations while considering the graph structure.

### Ambulance Selection

For each available ambulance, the system calculates a route to the incident and estimates the response time.

The ambulance with the lowest estimated travel time is selected for dispatch.

### Hospital Selection

The system evaluates available hospitals and selects a suitable destination based on the emergency type and routing information.

## 🛠️ Tech Stack

### Frontend

- React
- Vite
- JavaScript
- Axios
- CSS

### Backend

- Python
- FastAPI
- Pydantic
- Pytest

### Algorithms

- A* Search
- Graph-based route planning
- Resource selection based on estimated travel time

## 📁 Project Structure

```text
emergency-response-route-planner/
│
├── backend/
│   └── app/
│       ├── api/
│       ├── models/
│       ├── services/
│       └── main.py
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json
│
├── tests/
│
├── requirements.txt
├── README.md
└── .gitignore
```

## 🔌 API Endpoints

### Incidents

```text
POST /api/incidents
```

Creates a new emergency incident.

### Ambulances

```text
GET /api/ambulances
GET /api/ambulances/available
GET /api/ambulances/{ambulance_id}
```

Retrieves ambulance information and availability.

### Response Planning

```text
POST /api/response/{incident_id}
```

Generates an emergency response plan including ambulance and hospital routing.

### Dispatch

```text
POST /api/dispatch/{incident_id}
```

Dispatches the selected ambulance to the incident.

### Incident Lifecycle

```text
POST /api/incidents/{incident_id}/arrive
POST /api/incidents/{incident_id}/transport
POST /api/incidents/{incident_id}/resolve
```

Updates the incident throughout the emergency response lifecycle.

## 🚀 Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/autistickyrios/emergency-response-route-planner.git
cd emergency-response-route-planner
```

### 2. Set up the backend

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it in Git Bash:

```bash
source .venv/Scripts/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI server:

```bash
uvicorn backend.app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

### 3. Start the frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

## 🧪 Testing

Run the backend tests:

```bash
python -m pytest
```

Build the frontend:

```bash
npm run build
```

## 🎯 Example Emergency

Example incident:

```json
{
  "emergency_type": "accident",
  "severity": "critical",
  "location": "junction_05",
  "description": "Major road accident"
}
```

The system then:

1. Creates the emergency incident
2. Generates a response plan
3. Finds the best available ambulance
4. Calculates the route to the incident
5. Dispatches the ambulance
6. Tracks ambulance arrival
7. Begins patient transport
8. Selects a suitable hospital
9. Calculates the hospital route
10. Resolves the incident and makes the ambulance available again

## 🔮 Future Scope

Possible future improvements include:

- Real-time map integration
- Live traffic data
- GPS-based ambulance tracking
- Database persistence
- Machine-learning-based ETA prediction
- Multi-ambulance coordination
- Real-time notifications
- Authentication and role-based access
- Cloud deployment
- Dynamic hospital capacity tracking

## 👨‍💻 Project

**Emergency Response Route Planner**

Built as an academic full-stack software development project demonstrating emergency resource allocation, graph algorithms, API development, and frontend-backend integration.
