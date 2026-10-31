function EvidenceTab({ evidence = [], sources = [] }) {
  return (
    <div className="fade-in tab-panel">
      {sources.length > 0 && (
        <div className="sources-bar">
          <span className="sources-label">Contributing Agents:</span>
          {sources.map((s, i) => (
            <span key={i} className="source-chip">
              {s.replace(/_/g, " ")}
            </span>
          ))}
        </div>
      )}

      {evidence.length > 0 ? (
        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>Metric / Indicator</th>
                <th>Observed Value</th>
                <th>Device / Segment</th>
                <th>Interpretation</th>
              </tr>
            </thead>
            <tbody>
              {evidence.map((e, i) => (
                <tr key={i}>
                  <td className="font-medium">{e.metric || "—"}</td>
                  <td className="text-red">{e.value ?? "—"}</td>
                  <td>{e.device || "—"}</td>
                  <td className="text-muted">{e.interpretation || "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p className="text-muted">No supporting evidence available.</p>
      )}
    </div>
  );
}

export default EvidenceTab;