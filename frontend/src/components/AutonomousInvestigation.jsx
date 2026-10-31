
import React from "react";
import {
  Activity,
  CheckCircle2,
  Clock,
  Network,
  ShieldCheck,
  XCircle,
} from "lucide-react";

const AutonomousInvestigation = ({ investigation = {} }) => {
  const diagnostics = investigation.diagnostic_results || [];
  const telemetry = investigation.normalized_telemetry || {};

  const getStatus = (test) => {
    if (test.status === "not_configured") return "not-configured";
    if (test.success === true) return "success";
    if (test.success === false) return "failed";
    return "unknown";
  };

  const getIcon = (status) => {
    if (status === "success") return <CheckCircle2 size={18} />;
    if (status === "failed") return <XCircle size={18} />;
    if (status === "not-configured") return <Clock size={18} />;
    return <Activity size={18} />;
  };

  const getLabel = (test) => {
    const labels = {
      ping: "Ping Test",
      dns_resolution: "DNS Resolution",
      packet_loss: "Packet Loss",
      latency: "Latency Measurement",
      network_interfaces: "Network Interfaces",
      bandwidth: "Bandwidth Measurement",
    };

    return labels[test.test_name] || test.test_name || "Diagnostic Test";
  };

  return (
    <div className="autonomous-investigation">
      <div className="autonomous-investigation-header">
        <div>
          <span className="autonomous-investigation-label">
            <Activity size={14} />
            AUTONOMOUS ENGINE
          </span>

          <h3>Investigation Results</h3>

          <p>
            Network diagnostics performed by the investigation engine.
          </p>
        </div>

        <span className="autonomous-investigation-status">
          {investigation.investigation_status || "Unknown"}
        </span>
      </div>

      <div className="autonomous-telemetry">
        <div>
          <span>Latency</span>
          <strong>
            {telemetry.latency ?? "N/A"}
            {telemetry.latency != null ? " ms" : ""}
          </strong>
        </div>

        <div>
          <span>Packet Loss</span>
          <strong>
            {telemetry.packet_loss ?? "N/A"}
            {telemetry.packet_loss != null ? "%" : ""}
          </strong>
        </div>

        <div>
          <span>Jitter</span>
          <strong>
            {telemetry.jitter ?? "N/A"}
            {telemetry.jitter != null ? " ms" : ""}
          </strong>
        </div>

        <div>
          <span>DNS</span>
          <strong>{telemetry.dns_status || "N/A"}</strong>
        </div>
      </div>

      <div className="autonomous-diagnostics">
        <div className="autonomous-diagnostics-title">
          <Network size={18} />
          <h4>Executed Diagnostics</h4>
          <span>{diagnostics.length} Tests</span>
        </div>

        {diagnostics.length > 0 ? (
          diagnostics.map((test, index) => {
            const status = getStatus(test);

            return (
              <div
                className={`autonomous-diagnostic-row ${status}`}
                key={`${getLabel(test)}-${index}`}
              >
                <div className="autonomous-diagnostic-icon">
                  {getIcon(status)}
                </div>

                <div className="autonomous-diagnostic-content">
                  <strong>{getLabel(test)}</strong>

                  <p>
                    {test.message ||
                      test.error ||
                      test.status ||
                      (test.success
                        ? "Test completed successfully"
                        : "No test details available")}
                  </p>
                </div>

                <span className="autonomous-diagnostic-status">
                  {status.replaceAll("-", " ")}
                </span>
              </div>
            );
          })
        ) : (
          <p>No diagnostic results available.</p>
        )}
      </div>

      <div className="autonomous-safety">
        <ShieldCheck size={19} />

        <div>
          <strong>Safe Diagnostic Mode</strong>
          <p>
            Diagnostics do not automatically modify network configurations.
            Human approval is required for configuration changes.
          </p>
        </div>
      </div>
    </div>
  );
};

export default AutonomousInvestigation;
