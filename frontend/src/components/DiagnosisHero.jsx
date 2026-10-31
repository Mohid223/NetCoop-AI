function DiagnosisHero({ report }) {
  const isInsufficient =
    report.status === "insufficient_evidence" ||
    report.status === "insufficient evidence";

  return (
    <div className="diagnosis-hero">
      <div className="device-visual">
        <div className="router-illustration">
          <div className="router-body">
            <div className="antenna left"></div>
            <div className="antenna right"></div>
            <div className="wifi-waves"></div>
            <div className="leds">
              <span></span>
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
          <div className="check-badge">✓</div>
        </div>
      </div>

      <div className="diagnosis-content">
        <div className={`root-cause-card ${isInsufficient ? "warning" : ""}`}>
          <div className="cause-header">
            <span className="warning-icon">{isInsufficient ? "⚠️" : "🚨"}</span>
            <h3>Probable Root Cause</h3>
          </div>
          <p>{report.suspected_root_cause || "No root cause identified"}</p>
        </div>

        <div className="quick-insight">
          <span className="insight-icon">💡</span>
          <span>
            {report.supporting_evidence?.[0]?.interpretation ||
              "Analysis completed by multi-agent system"}
          </span>
        </div>
      </div>
    </div>
  );
}

export default DiagnosisHero;