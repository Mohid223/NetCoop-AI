function ChatTab({ log = [] }) {
  return (
    <div className="fade-in tab-panel">
      <p className="text-muted mb-4">
        Showing {log.length} structured messages exchanged between agents.
      </p>
      <div className="chat-log">
        {log.map((m, i) => {
          const isError = m.msg_type === "ERROR";
          const isResult = m.msg_type === "RESULT";
          return (
            <div
              key={i}
              className={`chat-msg ${isError ? "error" : isResult ? "result" : ""}`}
            >
              <div className="chat-header">
                <span className="sender">{m.sender}</span>
                <span className="arrow">➔</span>
                <span className="recipient">{m.recipient}</span>
                <span className="type-badge">{m.msg_type}</span>
              </div>
              <div className="chat-body">
                {m.payload?.anomalies?.length > 0 && (
                  <div className="chat-data">
                    Anomalies Detected:{" "}
                    <span className="code">
                      {m.payload.anomalies.join(", ")}
                    </span>
                  </div>
                )}
                {m.payload?.error && (
                  <div className="chat-data text-red">
                    Data Error: {m.payload.error}
                  </div>
                )}
                {m.payload?.suspected_root_cause && (
                  <div className="chat-data text-green">
                    Final Conclusion: {m.payload.suspected_root_cause}
                  </div>
                )}
                {m.confidence != null && (
                  <div className="chat-meta">
                    Confidence: {Math.round(m.confidence * 100)}%
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default ChatTab;