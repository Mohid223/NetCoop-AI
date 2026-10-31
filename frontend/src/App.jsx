import { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import MetricsRow from "./components/MetricsRow";
import DiagnosisHero from "./components/DiagnosisHero";
import AffectedDevices from "./components/AffectedDevices";
import RecommendedActions from "./components/RecommendedActions";

import DiagnosisTab from "./pages/DiagnosisTab";
import ChatTab from "./pages/ChatTab";
import EvidenceTab from "./pages/EvidenceTab";
import JsonTab from "./pages/JsonTab";

const API = "http://127.0.0.1:8000";

function App() {
  const [scenarios, setScenarios] = useState([]);
  const [selected, setSelected] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [tab, setTab] = useState("diagnosis");
  const [isLive, setIsLive] = useState(false);
  const [activeAgent, setActiveAgent] = useState(-1);

  useEffect(() => {
    axios
      .get(`${API}/api/scenarios`)
      .then((res) => {
        setScenarios(res.data.scenarios || []);
        if (res.data.scenarios?.length > 0) {
          setSelected(res.data.scenarios[0]);
        }
      })
      .catch((err) => console.error("API Error:", err));
  }, []);

  const simulatePipeline = () => {
    setActiveAgent(0);
    const intervals = [800, 1600, 2400, 3200, 4000];
    intervals.forEach((time, index) => {
      setTimeout(() => setActiveAgent(index), time);
    });
    setTimeout(() => setActiveAgent(-1), 4800);
  };

  const runDiagnosis = async () => {
    setLoading(true);
    setResult(null);
    setIsLive(false);
    simulatePipeline();

    try {
      const res = await axios.post(`${API}/api/run`, {
        scenario_file: selected,
      });
      setResult(res.data);
      setTab("diagnosis");
    } catch (err) {
      alert("Error: " + err.message);
    }
    setTimeout(() => setLoading(false), 4500);
  };

  const runLiveDiagnosis = async () => {
    setLoading(true);
    setResult(null);
    setIsLive(true);
    simulatePipeline();

    try {
      const res = await axios.post(`${API}/api/run-live`);
      setResult(res.data);
      setTab("diagnosis");
    } catch (err) {
      alert("Error: " + err.message);
    }
    setTimeout(() => setLoading(false), 4500);
  };

  return (
    <div className="app">
      <Sidebar
        scenarios={scenarios}
        selected={selected}
        setSelected={setSelected}
        loading={loading}
        isLive={isLive}
        activeAgent={activeAgent}
        onRunDiagnosis={runDiagnosis}
        onRunLive={runLiveDiagnosis}
      />

      <div className="main-wrapper">
        <Header />

        <main className="main">
          {!result && !loading && (
            <div className="empty-state">
              <div className="hero-icon">🛡️</div>
              <h2>System Ready</h2>
              <p>
                Select a simulated scenario or run a live network diagnostic.
                The agents will collaborate to find the root cause.
              </p>
            </div>
          )}

          {loading && (
            <div className="loading-state">
              <div className="spinner"></div>
              <h3>
                {isLive
                  ? "Analyzing Live Network..."
                  : "Agents are communicating..."}
              </h3>
              <p>Please wait while the multi-agent system correlates evidence.</p>
            </div>
          )}

          {result && !loading && (
            <div className="results-container fade-in">
              {isLive && (
                <div className="live-banner">
                   Live Diagnosis: Data collected via real ping test from your host machine.
                </div>
              )}

              {(result.report.status === "insufficient_evidence" ||
                result.report.status === "insufficient evidence") && (
                <div className="warning-banner">
                    Notice: No significant anomalies found. System is operating normally.
                </div>
              )}

              <MetricsRow report={result.report} />

              <DiagnosisHero report={result.report} />

              <div className="bottom-grid">
                <AffectedDevices devices={result.report.affected_devices || []} />
                <RecommendedActions actions={result.report.recommended_actions || []} />
              </div>

              {/* Tabs */}
              <div className="tabs">
                <button
                  className={tab === "diagnosis" ? "tab active" : "tab"}
                  onClick={() => setTab("diagnosis")}
                >
                    Diagnosis
                </button>
                <button
                  className={tab === "chat" ? "tab active" : "tab"}
                  onClick={() => setTab("chat")}
                >
                  Agent Chat Log
                </button>
                <button
                  className={tab === "evidence" ? "tab active" : "tab"}
                  onClick={() => setTab("evidence")}
                >
                   Evidence Data
                </button>
                <button
                  className={tab === "json" ? "tab active" : "tab"}
                  onClick={() => setTab("json")}
                >
                   Raw JSON
                </button>
              </div>

              <div className="tab-content">
                {tab === "diagnosis" && <DiagnosisTab report={result.report} />}
                {tab === "chat" && <ChatTab log={result.message_log || []} />}
                {tab === "evidence" && (
                  <EvidenceTab
                    evidence={result.report.supporting_evidence || []}
                    sources={result.report.evidence_sources || []}
                  />
                )}
                {tab === "json" && <JsonTab report={result.report} />}
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;