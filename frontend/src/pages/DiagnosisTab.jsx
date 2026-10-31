function DiagnosisTab({ report }) {
  return (
    <div className="fade-in tab-panel">
      {/* Alternative Causes */}
      {report.alternative_causes?.length > 0 && (
        <div className="section">
          <h3>Alternative Causes Considered</h3>
          <ul className="alt-list">
            {report.alternative_causes.map((cause, i) => (
              <li key={i}>{cause}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Limitations */}
      {report.limitations?.length > 0 && (
        <div className="section">
          <h3>Limitations & Uncertainty</h3>
          <ul className="limitations-list">
            {report.limitations.map((item, i) => (
              <li key={i}>
                <span className="limitation-icon">⚠️</span>
                {item}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Evidence Sources */}
      {report.evidence_sources?.length > 0 && (
        <div className="section">
          <h3>Evidence Sources (Agents)</h3>
          <div className="sources-chips">
            {report.evidence_sources.map((source, i) => (
              <span key={i} className="source-chip">
                {source.replace(/_/g, " ")}
              </span>
            ))}
          </div>
        </div>
      )}

      {!report.alternative_causes?.length &&
        !report.limitations?.length &&
        !report.evidence_sources?.length && (
          <p className="text-muted">
            No additional diagnostic details available.
          </p>
        )}
    </div>
  );
}

export default DiagnosisTab;