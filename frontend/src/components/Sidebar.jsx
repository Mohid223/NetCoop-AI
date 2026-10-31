import AgentPipeline from "./AgentPipeline";

const agents = [
  { name: "Performance", icon: "📊" },
  { name: "Infrastructure", icon: "🖥️" },
  { name: "Connectivity", icon: "📡" },
  { name: "Correlation", icon: "🎯" },
  { name: "Reporting", icon: "📝" },
];

function Sidebar({
  scenarios,
  selected,
  setSelected,
  loading,
  isLive,
  activeAgent,
  onRunDiagnosis,
  onRunLive,
}) {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="logo">
          <div className="logo-icon"></div>
          <div>
            <div className="logo-text">NetCoop AI</div>
            <div className="logo-sub">Network Diagnostic System</div>
          </div>
        </div>
      </div>

      <nav className="nav">
        <button className="nav-item active">
          <span className="nav-icon"></span>
          <span>Dashboard</span>
        </button>
        <button className="nav-item">
          <span className="nav-icon"></span>
          <span>Live Network</span>
        </button>
        <button className="nav-item">
          <span className="nav-icon"></span>
          <span>Performance</span>
        </button>
        <button className="nav-item">
          <span className="nav-icon"></span>
          <span>Infrastructure</span>
        </button>
        <button className="nav-item">
          <span className="nav-icon"></span>
          <span>Connectivity</span>
        </button>
        <button className="nav-item">
          <span className="nav-icon"></span>
          <span>Reporting</span>
        </button>
      </nav>

      <div className="sidebar-controls">
        <div className="control-group">
          <label>Simulated Scenarios</label>
          <select
            value={selected}
            onChange={(e) => setSelected(e.target.value)}
            disabled={loading}
          >
            {scenarios.map((s) => (
              <option key={s} value={s}>
                {s.replace(".json", "").replace(/_/g, " ")}
              </option>
            ))}
          </select>
        </div>

        <button
          className="run-btn primary"
          onClick={onRunDiagnosis}
          disabled={loading || !selected}
        >
          {loading && !isLive ? "Analyzing..." : "Run Simulated Scenario"}
        </button>

        <div className="divider">OR</div>

        <button
          className="run-btn live"
          onClick={onRunLive}
          disabled={loading}
        >
          {loading && isLive ? "Pinging Network..." : " Check Live Network"}
        </button>
      </div>

      <AgentPipeline agents={agents} activeAgent={activeAgent} />

      <div className="sidebar-footer">
        <p>
          Smarter Network.
          <br />
          Stronger Connection.
        </p>
      </div>
    </aside>
  );
}

export default Sidebar;