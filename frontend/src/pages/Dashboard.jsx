/* eslint-disable react-hooks/set-state-in-effect */
import { useEffect, useMemo, useState } from "react";
import {
  ambulanceArrived,
  beginTransport,
  createIncident,
  dispatchIncident,
  generateResponsePlan,
  getAmbulances,
  resolveIncident,
} from "../services/api";
import "./Dashboard.css";

const locationNames = {
  junction_01: "North Junction",
  junction_02: "East Junction",
  junction_03: "South Junction",
  junction_04: "West Junction",
  junction_05: "Central Junction",
};

const lifecycle = [
  ["active", "Reported"],
  ["dispatched", "Dispatched"],
  ["at_scene", "At scene"],
  ["transporting", "Transporting"],
  ["resolved", "Resolved"],
];

const formatLabel = (value = "") => value.replaceAll("_", " ");

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
      setError("");
    } catch (err) {
      console.error(err);
      setError("Unable to load ambulance data.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { refreshAmbulances(); }, []);

  const runAction = async (action, success) => {
    if (!incident) return;
    try {
      setActionLoading(true); setError(""); setMessage("");
      await action(incident.id);
      setIncident((current) => ({ ...current, status: success.status }));
      setMessage(success.message);
      await refreshAmbulances();
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "Unable to update incident.");
    } finally { setActionLoading(false); }
  };

  const handleCreateIncident = async (event) => {
    event.preventDefault();
    try {
      setActionLoading(true); setError(""); setMessage(""); setResponsePlan(null);
      const data = await createIncident({ emergency_type: emergencyType, severity, location, description });
      setIncident(data); setMessage(`Incident ${data.id} created successfully.`);
    } catch (err) {
      console.error(err); setError(err.response?.data?.detail || "Unable to create incident.");
    } finally { setActionLoading(false); }
  };

  const handleGenerateResponse = async () => {
    if (!incident) return;
    try {
      setActionLoading(true); setError(""); setMessage("");
      const data = await generateResponsePlan(incident.id);
      setResponsePlan(data);
      await dispatchIncident(incident.id);
      setIncident((current) => ({ ...current, status: "dispatched", assigned_ambulance_id: data.ambulance.id }));
      setMessage("AI response plan generated and ambulance dispatched.");
      await refreshAmbulances();
    } catch (err) {
      console.error(err); setError(err.response?.data?.detail || "Unable to generate response plan.");
    } finally { setActionLoading(false); }
  };

  const counts = useMemo(() => ({
    available: ambulances.filter((item) => item.status === "available").length,
    dispatched: ambulances.filter((item) => item.status === "dispatched").length,
    busy: ambulances.filter((item) => item.status === "busy").length,
    offline: ambulances.filter((item) => item.status === "offline").length,
  }), [ambulances]);

  const currentStep = Math.max(0, lifecycle.findIndex(([status]) => status === incident?.status));
  const currentAction = {
    active: [handleGenerateResponse, "Generate & dispatch response"],
    dispatched: [() => runAction(ambulanceArrived, { status: "at_scene", message: "Ambulance has arrived at the scene." }), "Confirm ambulance arrived"],
    at_scene: [() => runAction(beginTransport, { status: "transporting", message: "Patient transport has started." }), "Begin patient transport"],
    transporting: [() => runAction(resolveIncident, { status: "resolved", message: "Emergency response completed." }), "Resolve incident"],
  }[incident?.status];

  if (loading) return <main className="loading-state"><span className="loader" />Loading operations console...</main>;

  return (
    <main className="dashboard-shell">
      <header className="topbar">
        <div className="brand-lockup"><div className="brand-mark">ER</div><div><p className="micro-label">OPERATIONS CONSOLE</p><h1>Emergency Response</h1></div></div>
        <div className="topbar-actions"><div className="system-state"><span className="live-dot" />System online <span className="divider" /> <span className="muted">Last sync just now</span></div><button className="button button-quiet" onClick={refreshAmbulances}>Refresh data</button></div>
      </header>

      {(error || message) && <div className={`notification ${error ? "notification-error" : "notification-success"}`} role="status">{error || message}</div>}

      <section className="hero-grid">
        <div className="hero-copy"><p className="micro-label accent">REAL-TIME DISPATCH</p><h2>Move faster when it matters.</h2><p className="hero-description">Coordinate every response from one live command center. Generate routes, assign crews, and close the loop with clarity.</p></div>
        <div className="hero-meta"><span className="meta-label">ACTIVE INCIDENT</span><strong>{incident ? incident.id : "NO ACTIVE CALL"}</strong><span>{incident ? `${formatLabel(incident.status)} · ${locationNames[incident.location] || incident.location}` : "Ready for dispatch"}</span></div>
      </section>

      <section className="metrics-grid" aria-label="Fleet overview">
        {[['available', 'Available units', 'Ready to dispatch'], ['dispatched', 'En route', 'Responding now'], ['busy', 'On assignment', 'Active support'], ['offline', 'Offline', 'Needs attention']].map(([key, label, note]) => <article className={`metric-card metric-${key}`} key={key}><div className="metric-marker" /><div><span>{label}</span><strong>{counts[key]}</strong><small>{note}</small></div></article>)}
      </section>

      <div className="content-grid">
        <section className="panel incident-panel"><div className="panel-heading"><div><p className="micro-label accent">01 / DISPATCH</p><h3>New emergency incident</h3></div><span className="panel-tag">INTAKE</span></div><form onSubmit={handleCreateIncident} className="incident-form">
          <label>Emergency type<select value={emergencyType} onChange={(event) => setEmergencyType(event.target.value)}><option value="accident">Road accident</option><option value="cardiac">Cardiac event</option><option value="fire">Fire response</option><option value="medical">Medical emergency</option></select></label>
          <label>Severity<select value={severity} onChange={(event) => setSeverity(event.target.value)}><option value="critical">Critical</option><option value="high">High</option><option value="medium">Medium</option><option value="low">Low</option></select></label>
          <label>Incident location<select value={location} onChange={(event) => setLocation(event.target.value)}>{Object.entries(locationNames).map(([value, name]) => <option value={value} key={value}>{name}</option>)}</select></label>
          <label>Call notes<input value={description} onChange={(event) => setDescription(event.target.value)} /></label>
          <button className="button button-primary" type="submit" disabled={actionLoading}><span>{actionLoading ? "Processing..." : "Create incident"}</span><b>→</b></button>
        </form></section>

        <section className="panel status-panel"><div className="panel-heading"><div><p className="micro-label accent">02 / LIVE STATUS</p><h3>Response lifecycle</h3></div><span className={`status-pill ${incident?.status || "standby"}`}>{incident ? formatLabel(incident.status) : "Standby"}</span></div>{incident ? <><div className="incident-summary"><div><span>Incident ID</span><strong>{incident.id}</strong></div><div><span>Priority</span><strong className="critical-text">{incident.severity}</strong></div><div><span>Location</span><strong>{locationNames[incident.location] || incident.location}</strong></div></div><div className="timeline">{lifecycle.map(([status, label], index) => <div className={`timeline-step ${index <= currentStep ? "complete" : ""} ${index === currentStep ? "current" : ""}`} key={status}><span className="timeline-dot">{index < currentStep ? "✓" : index + 1}</span><span>{label}</span></div>)}</div>{currentAction && <button className="button button-primary action-button" onClick={currentAction[0]} disabled={actionLoading}>{actionLoading ? "Updating response..." : currentAction[1]} <b>→</b></button>}{incident.status === "resolved" && <div className="resolved-note">Response complete. Unit released back to fleet.</div>}</> : <div className="empty-state"><div className="empty-icon">+</div><strong>Waiting for an incident</strong><p>Create a new incident to begin the response workflow.</p></div>}</section>
      </div>

      {responsePlan && <section className="panel route-panel"><div className="panel-heading"><div><p className="micro-label accent">03 / AI ROUTING</p><h3>Recommended response plan</h3></div><span className="panel-tag plan-tag">OPTIMIZED</span></div><div className="route-layout"><div className="route-map"><div className="map-grid" /><div className="route-line route-line-one" /><div className="route-line route-line-two" /><span className="map-point point-ambulance">A</span><span className="map-point point-incident">!</span><span className="map-point point-hospital">H</span><div className="map-caption">LIVE ROUTE GRAPH <span>·</span> {responsePlan.total_distance_km} KM TOTAL</div></div><div className="route-details"><div className="route-detail"><span>Assigned unit</span><strong>{responsePlan.ambulance.name}</strong><small>{responsePlan.ambulance.id} · {responsePlan.ambulance.crew_level} crew</small></div><div className="route-detail"><span>Destination</span><strong>{responsePlan.hospital.name}</strong><small>{responsePlan.hospital.location}</small></div><div className="route-stats"><div><span>ETA</span><strong>{responsePlan.total_estimated_time_minutes}<em> min</em></strong></div><div><span>Distance</span><strong>{responsePlan.total_distance_km}<em> km</em></strong></div></div></div></div></section>}

      <section className="panel fleet-panel"><div className="panel-heading"><div><p className="micro-label accent">04 / FLEET MONITOR</p><h3>Ambulance availability</h3></div><span className="panel-tag">{ambulances.length} UNITS</span></div><div className="fleet-table"><div className="fleet-row fleet-header"><span>UNIT</span><span>LOCATION</span><span>CREW</span><span>MEDICAL SUPPORT</span><span>STATUS</span></div>{ambulances.map((ambulance) => <div className="fleet-row" key={ambulance.id}><div className="unit-cell"><span className="unit-symbol">+</span><div><strong>{ambulance.name}</strong><small>{ambulance.id}</small></div></div><span>{locationNames[ambulance.location] || ambulance.location}</span><span>{ambulance.crew_level}</span><span>{ambulance.medical_support ? "Available" : "Not equipped"}</span><span><i className={`table-status ${ambulance.status}`} />{formatLabel(ambulance.status)}</span></div>)}</div></section>
      <footer className="footer"><span>Emergency Response Control Center</span><span>Secure operations environment <i className="live-dot" /></span></footer>
    </main>
  );
}

export default Dashboard;
