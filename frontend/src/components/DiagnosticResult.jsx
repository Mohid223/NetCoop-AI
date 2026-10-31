
import React from "react";
import {
  Activity,
  CheckCircle2,
  Clock,
  Network,
  XCircle,
  AlertCircle,
} from "lucide-react";

const DiagnosticResult = ({ diagnostic = {}, testName }) => {
  const success = diagnostic.success === true;
  const status = diagnostic.status || (success ? "passed" : "failed");

  const statusConfig = {
    passed: {
      icon: CheckCircle2,
      label: "Passed",
      className: "success",
    },
    success: {
      icon: CheckCircle2,
      label: "Success",
      className: "success",
    },
    failed: {
      icon: XCircle,
      label: "Failed",
      className: "danger",
    },
    not_configured: {
      icon: Clock,
      label: "Not Configured",
      className: "warning",
    },
    pending: {
      icon: Clock,
      label: "Pending",
      className: "warning",
    },
  };

  const config = statusConfig[status] || {
    icon: AlertCircle,
    label: status.replaceAll("_", " "),
    className: "neutral",
  };

  const Icon = config.icon;

  const details = Object.entries(diagnostic).filter(
    ([key, value]) =>
      !["test_name", "success", "status", "message", "error"].includes(key) &&
      value !== null &&
      value !== undefined &&
      typeof value !== "object"
  );

  return (
    <div className={`diagnostic-result ${config.className}`}>
      <div className="diagnostic-result-header">
        <div className="diagnostic-result-icon">
          <Activity size={19} />
        </div>

        <div className="diagnostic-result-title">
          <h4>
            {testName ||
              diagnostic.test_name ||
              "Network Diagnostic Test"}
          </h4>

          <p>
            {diagnostic.message ||
              diagnostic.error ||
              "No additional information provided."}
          </p>
        </div>

        <span className="diagnostic-result-status">
          <Icon size={15} />
          {config.label}
        </span>
      </div>

      {details.length > 0 && (
        <div className="diagnostic-result-details">
          {details.map(([key, value]) => (
            <div className="diagnostic-detail" key={key}>
              <span>{key.replaceAll("_", " ")}</span>
              <strong>{String(value)}</strong>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default DiagnosticResult;
