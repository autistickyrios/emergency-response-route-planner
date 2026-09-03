import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

export const getAmbulances = async () => {
  const response = await api.get("/api/ambulances");
  return response.data;
};

export const getHospitals = async () => {
  const response = await api.get("/api/hospitals");
  return response.data;
};

export const createIncident = async (incident) => {
  const response = await api.post("/api/incidents", incident);
  return response.data;
};

export const generateResponsePlan = async (incidentId) => {
  const response = await api.post(`/api/response/${incidentId}`);
  return response.data;
};

export const dispatchIncident = async (incidentId) => {
  const response = await api.post(`/api/dispatch/${incidentId}`);
  return response.data;
};

export const ambulanceArrived = async (incidentId) => {
  const response = await api.post(
    `/api/incidents/${incidentId}/arrive`
  );
  return response.data;
};

export const beginTransport = async (incidentId) => {
  const response = await api.post(
    `/api/incidents/${incidentId}/transport`
  );
  return response.data;
};

export const resolveIncident = async (incidentId) => {
  const response = await api.post(
    `/api/incidents/${incidentId}/resolve`
  );
  return response.data;
};

export default api;