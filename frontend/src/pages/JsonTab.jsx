function JsonTab({ report }) {
  const downloadReport = () => {
    const blob = new Blob([JSON.stringify(report, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${report.incident_id}_report.json`;
    a.click();
  };

  return (
    <div className="fade-in tab-panel">
      <div className="json-header">
        <p className="text-muted">
          Structured JSON output as required by the problem statement.
        </p>
        <button className="download-btn" onClick={downloadReport}>
          📥 Download Report
        </button>
      </div>
      <pre className="json-block">{JSON.stringify(report, null, 2)}</pre>
    </div>
  );
}

export default JsonTab;