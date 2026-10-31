function AgentPipeline({ agents, activeAgent }) {
  return (
    <div className="agents-pipeline">
      <h4>Agent Pipeline</h4>
      {agents.map((agent, index) => (
        <div
          key={agent.name}
          className={`pipeline-item ${activeAgent >= index ? "active" : ""}`}
        >
          <span className="agent-icon">{agent.icon}</span>
          <span className="agent-name">{agent.name}</span>
          {activeAgent === index && <span className="spinner-small"></span>}
          {activeAgent > index && <span className="check">✓</span>}
        </div>
      ))}
    </div>
  );
}

export default AgentPipeline;