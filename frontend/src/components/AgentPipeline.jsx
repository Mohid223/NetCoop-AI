function AgentPipeline({ messageLog = [], investigation = {} }) {
  const agents = [
    "Network Monitor",
    "Telemetry Analyzer",
    "Diagnostic Agent",
    "Root Cause Analyzer",
    "Recommendation Agent",
  ];

  const logs = Array.isArray(messageLog) ? messageLog : [];

  return (
    <section className="panel agent-panel">
      <div className="panel-heading">
        <div>
          <h2>Autonomous Agent Pipeline</h2>
          <p>AI agents working through the investigation</p>
        </div>
        <span className="pipeline-mode">
          {investigation.mode || "Autonomous"}
        </span>
      </div>

      <div className="agent-list">
        {agents.map((agent, index) => (
          <div className="agent-step" key={agent}>
            <div className="agent-number">{index + 1}</div>
            <div className="agent-info">
              <strong>{agent}</strong>
              <span>
                {index < logs.length ? "Activity recorded" : "Awaiting activity"}
              </span>
            </div>
            <span className="agent-indicator">
              {index < logs.length ? "●" : "○"}
            </span>
          </div>
        ))}
      </div>

      <div className="agent-logs">
        <h3>Investigation Activity</h3>

        {logs.length > 0 ? (
          logs.map((log, index) => {
            const message =
              typeof log === "string"
                ? log
                : log.message || log.content || JSON.stringify(log);

            return (
              <div className="agent-log" key={index}>
                <span className="log-bullet">›</span>
                <p>{message}</p>
              </div>
            );
          })
        ) : (
          <p className="empty-state">No agent activity available yet.</p>
        )}
      </div>
    </section>
  );
}

export default AgentPipeline;