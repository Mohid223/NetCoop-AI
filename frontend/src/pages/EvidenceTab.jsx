function EvidenceTab({ report = {}, investigation = {} }) {
  const evidence = Array.isArray(report.evidence) ? report.evidence : [];

  const telemetry = investigation.telemetry || {};
  const diagnosticTests = Array.isArray(investigation.diagnostic_tests)
    ? investigation.diagnostic_tests
    : [];

  const coverage = investigation.evidence_coverage || {};

  return (
    <div className="evidence-page">
      <section className="panel">
        <div className="panel-heading">
          <div>
            <h2>Evidence Analysis</h2>
            <p>Information collected during network investigation</p>
          </div>
          <span className="count-badge">{evidence.length} items</span>
        </div>

        {evidence.length > 0 ? (
          <div className="evidence-list">
            {evidence.map((item, index) => {
              const title =
                typeof item === "string"
                  ? item
                  : item.title || item.name || `Evidence ${index + 1}`;

              const description =
                typeof item === "object"
                  ? item.description || item.value || item.details || ""
                  : "";

              return (
                <article className="evidence-item" key={index}>
                  <div className="evidence-icon">◈</div>
                  <div>
                    <strong>{title}</strong>
                    {description && <p>{String(description)}</p>}
                  </div>
                </article>
              );
            })}
          </div>
        ) : (
          <div className="empty-state">
            <p>No supporting evidence was identified.</p>
            <small>Additional network telemetry is required.</small>
          </div>
        )}
      </section>

      <section className="panel">
        <div className="panel-heading">
          <div>
            <h2>Telemetry Snapshot</h2>
            <p>Available network measurements</p>
          </div>
        </div>

        {Object.keys(telemetry).length > 0 ? (
          <div className="telemetry-grid">
            {Object.entries(telemetry).map(([key, value]) => (
              <div className="telemetry-item" key={key}>
                <span>{key.replaceAll("_", " ")}</span>
                <strong>
                  {value === null || value === undefined
                    ? "Unavailable"
                    : typeof value === "object"
                      ? JSON.stringify(value)
                      : String(value)}
                </strong>
              </div>
            ))}
          </div>
        ) : (
          <p className="empty-state">No telemetry snapshot available.</p>
        )}
      </section>

      <section className="panel">
        <div className="panel-heading">
          <div>
            <h2>Diagnostic Tests</h2>
            <p>Tests included in the investigation</p>
          </div>
          <span className="count-badge">{diagnosticTests.length}</span>
        </div>

        {diagnosticTests.length > 0 ? (
          <div className="test-list">
            {diagnosticTests.map((test, index) => (
              <div className="test-item" key={index}>
                <span>✓</span>
                <p>
                  {typeof test === "string"
                    ? test
                    : test.name || test.test_name || JSON.stringify(test)}
                </p>
              </div>
            ))}
          </div>
        ) : (
          <p className="empty-state">No diagnostic test details available.</p>
        )}
      </section>

      <section className="panel">
        <h2>Evidence Coverage</h2>
        <pre className="json-content">
          {JSON.stringify(coverage, null, 2)}
        </pre>
      </section>
    </div>
  );
}

export default EvidenceTab;