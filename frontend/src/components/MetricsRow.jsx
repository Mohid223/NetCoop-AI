function MetricsRow({ report = {} }) {
  const confidence = report.confidence ?? 0;
  const affectedDevices = report.affected_devices?.length ?? 0;
  const evidence = report.evidence?.length ?? 0;
  const status = report.status || "No report";

  const metrics = [
    {
      label: "Confidence",
      value: `${Math.round(Number(confidence) * 100)}%`,
      icon: "◉",
    },
    {
      label: "Affected Devices",
      value: affectedDevices,
      icon: "▣",
    },
    {
      label: "Evidence Items",
      value: evidence,
      icon: "◈",
    },
    {
      label: "Diagnosis Status",
      value: status.replaceAll("_", " "),
      icon: "◎",
    },
  ];

  return (
    <section className="metrics-row">
      {metrics.map((metric) => (
        <article className="metric-card" key={metric.label}>
          <div className="metric-top">
            <span>{metric.label}</span>
            <span className="metric-icon">{metric.icon}</span>
          </div>
          <h2>{metric.value}</h2>
        </article>
      ))}
    </section>
  );
}

export default MetricsRow;