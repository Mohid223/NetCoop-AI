
function MetricsRow({ report }) {
  const confidence = Math.round((report.confidence || 0) * 100);
  const status = (report.status || "unknown").replace(/_/g, " ").toUpperCase();

  return (
    <div className="metrics-row">
      {/* Incident ID */}
      <div className="metric-card center-text">
        <div className="metric-icon blue"><Link2 size={24} /></div>
        <span className="metric-label">INCIDENT ID</span>
        <span className="metric-value big">{report.incident_id || "N/A"}</span>
      </div>

      {/* Confidence */}
      <div className="metric-card center-text">
        <div className="metric-icon green"><ShieldCheck size={24} /></div>
        <span className="metric-label">CONFIDENCE SCORE</span>
        <span className="metric-value big text-green">{confidence}% ↗</span>
      </div>

      {/* Status */}
      <div className="metric-card center-text">
        <div className="metric-icon purple"><HeartPulse size={24} /></div>
        <span className="metric-label">STATUS</span>
        <span className={`status-badge ${report.status}`}>{status}</span>
      </div>
    </div>
  );
}

export default MetricsRow;