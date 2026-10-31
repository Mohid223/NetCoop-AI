
import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 30000,
});

export const checkBackendHealth = async () => {
  const response = await api.get("/api/health");
  return response.data;
};

export const getScenarios = async () => {
  const response = await api.get("/api/scenarios");
  return response.data;
};

export const runScenario = async (scenarioFile) => {
  const response = await api.post("/api/run", {
    scenario_file: scenarioFile,
  });
  return response.data;
};

export const runLiveDiagnosis = async () => {
  const response = await api.post("/api/run-live");
  return response.data;
};

export default api;
