function DiagnosisHero({ report = {} }) {
  const status = report.status || "waiting";
  const rootCause =
    report.suspected_root_cause ||
    report.root_cause ||
    "Root cause not determined yet";

  const isInconclusive = status === "insufficient_evidence";

  return (
    <section className="diagnosis-hero">
      <div className="hero-content">
        <div className="hero-eyebrow">
          <span className="hero-pulse" />
          NETWORK DIAGNOSIS
        </div>

        <h1>Network Intelligence Center</h1>

        <p>
          Monitor network health, investigate incidents, and identify
          possible root causes using autonomous AI agents.
        </p>

        <div className="hero-diagnosis">
          <span className="hero-label">Current assessment</span>
          <h2>{rootCause}</h2>

          <span
            className={`diagnosis-status ${
              isInconclusive ? "warning" : "success"
            }`}
          >
            {status.replaceAll("_", " ").toUpperCase()}
          </span>
        </div>
      </div>
    </section>
  );
}

export default DiagnosisHero;