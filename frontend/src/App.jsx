
import { useEffect, useState } from "react";
import axios from "axios";

import Header from "./components/Header";
import Sidebar from "./components/Sidebar";
import MetricsRow from "./components/MetricsRow";
import DiagnosisHero from "./components/DiagnosisHero";
import AgentPipeline from "./components/AgentPipeline";
import AffectedDevices from "./components/AffectedDevices";
import RecommendedActions from "./components/RecommendedActions";

import ChatTab from "./pages/ChatTab";
import DiagnosisTab from "./pages/DiagnosisTab";
import EvidenceTab from "./pages/EvidenceTab";
import JsonTab from "./pages/JsonTab";

import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [activeTab, setActiveTab] = useState("diagnosis");
  const [scenarios, setScenarios] = useState([]);
  const [selectedScenario, setSelectedScenario] = useState("");
  const [result, setResult] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [backendStatus, setBackendStatus] = useState("checking");

  // Check backend connection
  useEffect(() => {
    checkBackend();
    loadScenarios();
  }, []);

  const checkBackend = async () => {
    try {
      await axios.get(`${API_URL}/api/health`);
      setBackendStatus("connected");
    } catch {
      setBackendStatus("disconnected");
    }
  };

  // Load available scenarios
  const loadScenarios = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/scenarios`);

      const data = response.data;
      const scenarioList = Array.isArray(data)
        ? data
        : data.scenarios || [];

      setScenarios(scenarioList);

      if (scenarioList.length > 0) {
        const first = scenarioList[0];

        setSelectedScenario(
          typeof first === "string"
            ? first
            : first.file || first.filename || first.name || ""
        );
      }
    } catch (err) {
      console.error("Scenario loading failed:", err);
    }
  };

  // Common API execution function
  const executeDiagnosis = async (endpoint, payload = {}) => {
    setLoading(true);
    setError("");

    try {
      const response = await axios.post(
        `${API_URL}${endpoint}`,
        payload,
        { timeout: 120000 }
      );

      setResult(response.data);
      setActiveTab("diagnosis");
      setBackendStatus("connected");
    } catch (err) {
      console.error("Diagnosis error:", err);

      setError(
        err.response?.data?.detail ||
        err.message ||
        "Unable to connect to the backend."
      );

      if (err.code === "ERR_NETWORK") {
        setBackendStatus("disconnected");
      }
    } finally {
      setLoading(false);
    }
  };

  // Run selected scenario
  const runScenario = () => {
    if (!selectedScenario) {
      setError("Please select a network scenario first.");
      return;
    }

    executeDiagnosis("/api/run", {
      scenario_file: selectedScenario,
    });
  };

  // Run autonomous live investigation
  const runLiveDiagnosis = () => {
    executeDiagnosis("/api/run-live");
  };

  const report = result?.report || {};
  const investigation = result?.autonomous_investigation || {};
  const messageLog = result?.message_log || [];

  const tabs = [
    { id: "diagnosis", label: "Diagnosis" },
    { id: "evidence", label: "Evidence" },
    { id: "chat", label: "AI Assistant" },
    { id: "json", label: "JSON Output" },
  ];

  return (
    <div className="app-container">
      <Header backendStatus={backendStatus} />

      <div className="app-layout">
        <Sidebar
          activeTab={activeTab}
          setActiveTab={setActiveTab}
        />

        <main className="main-content">
          <div className="dashboard-topbar">
            <div>
              <p className="dashboard-eyebrow">
                NETWORK INTELLIGENCE PLATFORM
              </p>
              <h1>NetCoop AI</h1>
              <p className="dashboard-description">
                Autonomous network monitoring, diagnosis and investigation.
              </p>
            </div>

            <div className="backend-indicator">
              <span
                className={`status-dot ${backendStatus}`}
              />
              {backendStatus === "connected"
                ? "Backend Connected"
                : backendStatus === "disconnected"
                  ? "Backend Disconnected"
                  : "Checking Backend"}
            </div>
          </div>

          {/* Execution Controls */}
          <section className="execution-panel">
            <div className="execution-heading">
              <div>
                <h2>Network Investigation</h2>
                <p>
                  Run a predefined scenario or start a live investigation.
                </p>
              </div>
            </div>

            <div className="execution-controls">
              <select
                value={selectedScenario}
                onChange={(e) => setSelectedScenario(e.target.value)}
                disabled={loading}
              >
                <option value="">Select a scenario</option>

                {scenarios.map((scenario, index) => {
                  const value =
                    typeof scenario === "string"
                      ? scenario
                      : scenario.file ||
                        scenario.filename ||
                        scenario.name;

                  return (
                    <option key={index} value={value}>
                      {typeof scenario === "string"
                        ? scenario
                        : scenario.name || value}
                    </option>
                  );
                })}
              </select>

              <button
                className="primary-action"
                onClick={runScenario}
                disabled={loading || !selectedScenario}
              >
                {loading ? "Running..." : "Run Scenario"}
              </button>

              <button
                className="live-action"
                onClick={runLiveDiagnosis}
                disabled={loading}
              >
                {loading ? "Investigating..." : "Run Live Investigation"}
              </button>
            </div>

            {loading && (
              <div className="loading-message">
                <span className="loading-spinner" />
                Autonomous agents are investigating the network...
              </div>
            )}

            {error && (
              <div className="error-message">
                {error}
              </div>
            )}
          </section>

          {/* Dashboard metrics */}
          {result && (
            <>
              <MetricsRow report={report} />

              <DiagnosisHero report={report} />

              <AgentPipeline
                messageLog={messageLog}
                investigation={investigation}
              />

              <div className="dashboard-grid">
                <AffectedDevices
                  devices={report.affected_devices || []}
                />

                <RecommendedActions
                  actions={report.recommended_actions || []}
                />
              </div>
            </>
          )}

          {/* Navigation Tabs */}
          <div className="content-tabs">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                className={
                  activeTab === tab.id
                    ? "content-tab active"
                    : "content-tab"
                }
                onClick={() => setActiveTab(tab.id)}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* Page Content */}
          <div className="tab-content">
            {!result && activeTab !== "chat" && (
              <div className="empty-dashboard">
                <h2>No Investigation Yet</h2>
                <p>
                  Run a scenario or start a live investigation to see
                  network diagnostic results here.
                </p>
              </div>
            )}

            {activeTab === "diagnosis" && result && (
              <DiagnosisTab
                report={report}
                investigation={investigation}
              />
            )}

            {activeTab === "evidence" && result && (
              <EvidenceTab
                report={report}
                investigation={investigation}
              />
            )}

            {activeTab === "chat" && (
              <ChatTab
                report={report}
                investigation={investigation}
                messageLog={messageLog}
              />
            )}

            {activeTab === "json" && result && (
              <JsonTab
                report={report}
                investigation={investigation}
                result={result}
              />
            )}
          </div>

          <footer className="app-footer">
            <span>NetCoop AI</span>
            <span>Autonomous Network Intelligence</span>
          </footer>
        </main>
      </div>
    </div>
  );
}

export default App;
