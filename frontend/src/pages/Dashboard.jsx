import { useEffect, useState } from "react";
import {
  getAmbulances,
  createIncident,
  generateResponsePlan,
  ambulanceArrived,
  beginTransport,
  resolveIncident,
} from "../services/api";
import "./Dashboard.css";

function Dashboard() {
  const [ambulances, setAmbulances] = useState([]);
  const [incident, setIncident] = useState(null);
  const [responsePlan, setResponsePlan] = useState(null);

  const [emergencyType, setEmergencyType] = useState("accident");
  const [severity, setSeverity] = useState("critical");
  const [location, setLocation] = useState("junction_05");
  const [description, setDescription] = useState("Major road accident");

  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const refreshAmbulances = async () => {
    try {
      const data = await getAmbulances();
      setAmbulances(data);
    } catch (err) {
      console.error(err);
      setError("Unable to load ambulance data.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    refreshAmbulances();
  }, []);

  const handleCreateIncident = async (event) => {
    event.preventDefault();

    try {
      setActionLoading(true);
      setError("");
      setMessage("");
      setResponsePlan(null);

      const data = await createIncident({
        emergency_type: emergencyType,
        severity,
        location,
        description,
      });

      setIncident(data);
      setMessage(`Incident ${data.id} created successfully.`);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "Unable to create incident.");
    } finally {
      setActionLoading(false);
    }
  };

  const handleGenerateResponse = async () => {
    if (!incident) return;

    try {
      setActionLoading(true);
      setError("");
      setMessage("");

      const data = await generateResponsePlan(incident.id);

      setResponsePlan(data);

      setIncident((current) => ({
        ...current,
        status: "dispatched",
        assigned_ambulance_id: data.ambulance.id,
      }));

      setMessage("AI response plan generated and ambulance dispatched.");
      await refreshAmbulances();
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.detail || "Unable to generate response plan."
      );
    } finally {
      setActionLoading(false);
    }
  };

  const handleArrive = async () => {
    if (!incident) return;

    try {
      setActionLoading(true);
      setError("");
      setMessage("");

      await ambulanceArrived(incident.id);

      setIncident((current) => ({
        ...current,
        status: "at_scene",
      }));

      setMessage("Ambulance has arrived at the scene.");
      await refreshAmbulances();
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "Unable to update incident.");
    } finally {
      setActionLoading(false);
    }
  };

  const handleTransport = async () => {
    if (!incident) return;

    try {
      setActionLoading(true);
      setError("");
      setMessage("");

      await beginTransport(incident.id);

      setIncident((current) => ({
        ...current,
        status: "transporting",
      }));

      setMessage("Patient transport has started.");
      await refreshAmbulances();
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "Unable to update incident.");
    } finally {
      setActionLoading(false);
    }
  };

  const handleResolve = async () => {
    if (!incident) return;

    try {
      setActionLoading(true);
      setError("");
      setMessage("");

      await resolveIncident(incident.id);

      setIncident((current) => ({
        ...current,
        status: "resolved",
      }));

      setMessage("Emergency response completed.");
      await refreshAmbulances();
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "Unable to resolve incident.");
    } finally {
      setActionLoading(false);
    }
  };

  const availableCount = ambulances.filter(
    (ambulance) => ambulance.status === "available"
  ).length;

  const dispatchedCount = ambulances.filter(
    (ambulance) => ambulance.status === "dispatched"
  ).length;

  const busyCount = ambulances.filter(
    (ambulance) => ambulance.status === "busy"
  ).length;

  const offlineCount = ambulances.filter(
    (ambulance) => ambulance.status === "offline"
  ).length;

  if (loading) {
    return <main><p>Loading dashboard...</p></main>;
  }

  return (
    <main>
      <header>
        <div>
          <p className="eyebrow">AI EMERGENCY RESPONSE SYSTEM</p>
          <h1>Emergency Response Control Center</h1>
          <p className="status-online">System Online</p>
        </div>

        <button onClick={refreshAmbulances}>
          Refresh
        </button>
      </header>

      {error && <div className="alert error">{error}</div>}
      {message && <div className="alert success">{message}</div>}

      <section className="stats">
        <div className="stat-card">
          <span>Available</span>
          <strong>{availableCount}</strong>
        </div>

        <div className="stat-card">
          <span>Dispatched</span>
          <strong>{dispatchedCount}</strong>
        </div>

        <div className="stat-card">
          <span>Busy</span>
          <strong>{busyCount}</strong>
        </div>

        <div className="stat-card">
          <span>Offline</span>
          <strong>{offlineCount}</strong>
        </div>
      </section>

      <section>
        <div className="section-heading">
          <div>
            <p className="eyebrow">DISPATCH</p>
            <h2>Create Emergency Incident</h2>
          </div>
        </div>

        <form onSubmit={handleCreateIncident}>
          <div className="form-field">
            <label>Emergency Type</label>
            <select
              value={emergencyType}
              onChange={(event) => setEmergencyType(event.target.value)}
            >
              <option value="accident">Accident</option>
              <option value="cardiac">Cardiac</option>
              <option value="fire">Fire</option>
              <option value="medical">Medical</option>
            </select>
          </div>

          <div className="form-field">
            <label>Severity</label>
            <select
              value={severity}
              onChange={(event) => setSeverity(event.target.value)}
            >
              <option value="critical">Critical</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
          </div>

          <div className="form-field">
            <label>Location</label>
            <select
              value={location}
              onChange={(event) => setLocation(event.target.value)}
            >
              <option value="junction_01">North Junction</option>
              <option value="junction_02">East Junction</option>
              <option value="junction_03">South Junction</option>
              <option value="junction_04">West Junction</option>
              <option value="junction_05">Central Junction</option>
            </select>
          </div>

          <div className="form-field">
            <label>Description</label>
            <input
              type="text"
              value={description}
              onChange={(event) => setDescription(event.target.value)}
            />
          </div>

          <button type="submit" disabled={actionLoading}>
            Create Incident
          </button>
        </form>
      </section>

      {incident && (
        <section>
          <div className="incident-header">
            <div>
              <p className="eyebrow">CURRENT INCIDENT</p>
              <h2>{incident.id}</h2>
            </div>

            <span className="badge">{incident.status}</span>
          </div>

          <div className="incident-details">
            <div>
              <span>Type</span>
              <strong>{incident.emergency_type}</strong>
            </div>

            <div>
              <span>Severity</span>
              <strong>{incident.severity}</strong>
            </div>

            <div>
              <span>Location</span>
              <strong>{incident.location}</strong>
            </div>
          </div>

          <div className="workflow">
            <div className={incident.status === "active" ? "step active" : "step"}>
              1. Active
            </div>

            <div className={incident.status === "dispatched" ? "step active" : "step"}>
              2. Dispatched
            </div>

            <div className={incident.status === "at_scene" ? "step active" : "step"}>
              3. At Scene
            </div>

            <div className={incident.status === "transporting" ? "step active" : "step"}>
              4. Transporting
            </div>

            <div className={incident.status === "resolved" ? "step active" : "step"}>
              5. Resolved
            </div>
          </div>

          <div className="action-area">
            {incident.status === "active" && (
              <button onClick={handleGenerateResponse} disabled={actionLoading}>
                Generate & Dispatch Response
              </button>
            )}

            {incident.status === "dispatched" && (
              <button onClick={handleArrive} disabled={actionLoading}>
                Ambulance Arrived
              </button>
            )}

            {incident.status === "at_scene" && (
              <button onClick={handleTransport} disabled={actionLoading}>
                Begin Transport
              </button>
            )}

            {incident.status === "transporting" && (
              <button onClick={handleResolve} disabled={actionLoading}>
                Resolve Incident
              </button>
            )}
          </div>
        </section>
      )}

      {responsePlan && (
        <section>
          <div className="section-heading">
            <div>
              <p className="eyebrow">AI ROUTING</p>
              <h2>Response Plan</h2>
            </div>
          </div>

          <div className="response-grid">
            <div className="response-card">
              <span>Assigned Ambulance</span>
              <strong>
                {responsePlan.ambulance.name}
              </strong>
              <p>{responsePlan.ambulance.id}</p>
            </div>

            <div className="response-card">
              <span>Destination Hospital</span>
              <strong>
                {responsePlan.hospital.name}
              </strong>
              <p>{responsePlan.hospital.location}</p>
            </div>

            <div className="response-card">
              <span>Route to Incident</span>
              <strong>
                {responsePlan.route_to_incident.path.join(" → ")}
              </strong>
              <p>
                {responsePlan.route_to_incident.distance_km} km ·{" "}
                {responsePlan.route_to_incident.estimated_time_minutes} min
              </p>
            </div>

            <div className="response-card">
              <span>Route to Hospital</span>
              <strong>
                {responsePlan.route_to_hospital.path.join(" → ")}
              </strong>
              <p>
                {responsePlan.route_to_hospital.distance_km} km ·{" "}
                {responsePlan.route_to_hospital.estimated_time_minutes} min
              </p>
            </div>
          </div>

          <div className="totals">
            <div>
              <span>Total Distance</span>
              <strong>{responsePlan.total_distance_km} km</strong>
            </div>

            <div>
              <span>Total Estimated Time</span>
              <strong>{responsePlan.total_estimated_time_minutes} min</strong>
            </div>
          </div>
        </section>
      )}

      <section>
        <div className="section-heading">
          <div>
            <p className="eyebrow">FLEET</p>
            <h2>Ambulances</h2>
          </div>
        </div>

        <div className="ambulance-grid">
          {ambulances.map((ambulance) => (
            <article className="ambulance-card" key={ambulance.id}>
              <div className="ambulance-top">
                <div>
                  <h3>{ambulance.name}</h3>
                  <span>{ambulance.id}</span>
                </div>

                <span className={`status ${ambulance.status}`}>
                  {ambulance.status}
                </span>
              </div>

              <p>
                <span>Location</span>
                {ambulance.location}
              </p>

              <p>
                <span>Crew</span>
                {ambulance.crew_level}
              </p>

              <p>
                <span>Medical Support</span>
                {ambulance.medical_support ? "Yes" : "No"}
              </p>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}

export default Dashboard;
