
import React from "react";
import {
  Activity,
  AlertTriangle,
  CheckCircle2,
  CircleHelp,
  Clock,
  Cpu,
  Database,
  Gauge,
  Network,
  ShieldCheck,
  XCircle,
  Zap,
} from "lucide-react";

import AutonomousInvestigation from "../components/AutonomousInvestigation";
import ConfidenceCard from "../components/ConfidenceCard";
import DiagnosticResult from "../components/DiagnosticResult";

const display = (value, suffix = "") => {
  if (value === null || value === undefined || value === "") {
    return "Not available";
  }

  return `${value}${suffix}`;
};

function Section({ title, icon: Icon, children }) {
  return (
    <section className="diagnosis-section">
      <div className="diagnosis-section-heading">
        {Icon && <Icon size={19} />}
        <h3>{title}</h3>
      </div>
      {children}
    </section>
  );
}

function Status({ value }) {
  const normalized = String(value || "unknown").toLowerCase();

  const success = [
    "success",
    "passed",
    "completed",
    "healthy",
    "true",
  ].includes(normalized);

  const warning = [
    "pending",
    "not_configured",
    "unknown",
    "inconclusive",
  ].includes(normalized);

  return (
    <span
      className={`diagnosis-status ${
        success ? "success" : warning ? "warning" : "danger"
      }`}
    >
      {success ? (
        <CheckCircle2 size={14} />
      ) : warning ? (
        <Clock size={14} />
      ) : (
        <XCircle size={14} />
      )}
      {normalized.replaceAll("_", " ")}
    </span>
  );
}

function TelemetryCard({ label, value, suffix, icon: Icon }) {
  return (
    <div className="diagnosis-telemetry-card">
      <div className="diagnosis-telemetry-heading">
        <span>{label}</span>
        <Icon size={18} />
      </div>

      <strong>{display(value, suffix)}</strong>
    </div>
  );
}

export default function DiagnosisTab({
  report = {},
  investigation = {},
}) {
  const telemetry = investigation.normalized_telemetry || {};
  const rootCause = investigation.root_cause_analysis || {};
  const confidence = investigation.confidence || {};
  const diagnostics = investigation.diagnostic_results || [];
  const plan = investigation.diagnostic_plan || {};
  const graph = investigation.causal_graph || {};

  const evidence = report.supporting_evidence || [];
  const alternatives = report.alternative_causes || [];
  const limitations = report.limitations || [];
  const sources = report.evidence_sources || [];
  const actions = report.recommended_actions || [];

  const diagnosticNames = {
    ping: "Ping Connectivity",
    dns_resolution: "DNS Resolution",
    packet_loss: "Packet Loss",
    latency: "Latency Test",
    network_interfaces: "Network Interfaces",
    bandwidth: "Bandwidth Test",
  };

  return (
    <div className="diagnosis-tab">

      {/* Investigation Overview */}
      <div className="diagnosis-page-header">
        <div>
          <span className="diagnosis-eyebrow">
            <Zap size={14} />
            AUTONOMOUS DIAGNOSTICS
          </span>

          <h2>Network Diagnosis</h2>

          <p>
            Network investigation results and diagnostic intelligence.
          </p>
        </div>

        <Status value={investigation.investigation_status} />
      </div>

      {/* Autonomous Investigation Component */}
      {Object.keys(investigation).length > 0 && (
        <AutonomousInvestigation investigation={investigation} />
      )}

      {/* Network Telemetry */}
      <Section title="Network Telemetry" icon={Activity}>
        <div className="diagnosis-telemetry-grid">
          <TelemetryCard
            label="Latency"
            value={telemetry.latency}
            suffix=" ms"
            icon={Activity}
          />

          <TelemetryCard
            label="Packet Loss"
            value={telemetry.packet_loss}
            suffix="%"
            icon={Network}
          />

          <TelemetryCard
            label="Jitter"
            value={telemetry.jitter}
            suffix=" ms"
            icon={Gauge}
          />

          <TelemetryCard
            label="CPU Usage"
            value={telemetry.cpu_usage}
            suffix="%"
            icon={Cpu}
          />

          <TelemetryCard
            label="Memory Usage"
            value={telemetry.memory_usage}
            suffix="%"
            icon={Database}
          />

          <TelemetryCard
            label="DNS Status"
            value={telemetry.dns_status}
            icon={ShieldCheck}
          />
        </div>
      </Section>

      {/* Diagnostic Results */}
      <Section title="Diagnostic Test Results" icon={Network}>
        {diagnostics.length > 0 ? (
          <div className="diagnosis-diagnostic-list">
            {diagnostics.map((test, index) => {
              const name =
                diagnosticNames[test.test_name] ||
                test.test_name ||
                `Diagnostic ${index + 1}`;

              return (
                <div
                  className="diagnosis-diagnostic-item"
                  key={`${name}-${index}`}
                >
                  <div className="diagnosis-diagnostic-info">
                    <strong>{name}</strong>

                    <p>
                      {test.message ||
                        test.error ||
                        test.status ||
                        (test.success
                          ? "Diagnostic completed successfully."
                          : "No additional details available.")}
                    </p>
                  </div>

                  <Status
                    value={
                      test.status ||
                      (test.success ? "passed" : "failed")
                    }
                  />
                </div>
              );
            })}
          </div>
        ) : (
          <p className="diagnosis-empty">
            No diagnostic tests have been recorded.
          </p>
        )}
      </Section>

      {/* Root Cause */}
      <Section title="Root Cause Analysis" icon={AlertTriangle}>
        <div className="diagnosis-root-card">
          <div className="diagnosis-root-top">
            <span>Analysis Status</span>
            <Status value={rootCause.status} />
          </div>

          <h3>
            {rootCause.primary_cause ||
              report.suspected_root_cause ||
              "Root cause not identified"}
          </h3>

          <p>
            {rootCause.message ||
              "There is not enough evidence to confirm a root cause."}
          </p>

          {rootCause.candidates?.length > 0 && (
            <div className="diagnosis-candidates">
              <strong>Possible Causes</strong>

              {rootCause.candidates.map((candidate, index) => (
                <div key={index}>
                  <CircleHelp size={15} />

                  {typeof candidate === "string"
                    ? candidate
                    : candidate.cause ||
                      candidate.name ||
                      JSON.stringify(candidate)}
                </div>
              ))}
            </div>
          )}
        </div>
      </Section>

      {/* Confidence Card */}
      <Section title="Evidence Confidence" icon={Gauge}>
        <ConfidenceCard confidence={confidence} />
      </Section>

      {/* Diagnostic Plan */}
      <Section title="Diagnostic Plan" icon={Zap}>
        <div className="diagnosis-plan-card">
          <div>
            <span>Plan Status</span>
            <strong>{plan.plan_status || "Not available"}</strong>
          </div>

          <div>
            <span>Execution Mode</span>
            <strong>{plan.execution_mode || "Not available"}</strong>
          </div>

          <div>
            <span>Suspected Cause</span>
            <strong>{plan.suspected_cause || "Not identified"}</strong>
          </div>

          {plan.planned_checks?.length > 0 && (
            <div className="diagnosis-planned-checks">
              <strong>Planned Checks</strong>

              {plan.planned_checks.map((check, index) => (
                <div key={index}>
                  <span>{check.test || "Diagnostic check"}</span>
                  <Status value={check.status} />
                </div>
              ))}
            </div>
          )}
        </div>
      </Section>

      {/* Causal Graph */}
      <Section title="Causal Graph" icon={Network}>
        <div className="diagnosis-graph-card">
          <div className="diagnosis-graph-count">
            <div>
              <strong>{graph.nodes?.length || 0}</strong>
              <span>Nodes</span>
            </div>

            <div>
              <strong>{graph.edges?.length || 0}</strong>
              <span>Connections</span>
            </div>
          </div>

          <p>
            {graph.interpretation ||
              "No supported causal relationships are currently available."}
          </p>
        </div>
      </Section>

      {/* Supporting Evidence */}
      <Section title="Supporting Evidence" icon={CheckCircle2}>
        {evidence.length > 0 ? (
          <ul className="diagnosis-bullet-list">
            {evidence.map((item, index) => (
              <li key={index}>
                {typeof item === "string"
                  ? item
                  : item.description ||
                    item.message ||
                    JSON.stringify(item)}
              </li>
            ))}
          </ul>
        ) : (
          <p className="diagnosis-empty">
            No supporting evidence available.
          </p>
        )}
      </Section>

      {/* Alternative Causes */}
      <Section title="Alternative Causes" icon={CircleHelp}>
        {alternatives.length > 0 ? (
          <ul className="diagnosis-bullet-list">
            {alternatives.map((item, index) => (
              <li key={index}>
                {typeof item === "string"
                  ? item
                  : item.cause ||
                    item.description ||
                    JSON.stringify(item)}
              </li>
            ))}
          </ul>
        ) : (
          <p className="diagnosis-empty">
            No alternative causes identified.
          </p>
        )}
      </Section>

      {/* Recommended Actions */}
      <Section title="Recommended Actions" icon={Zap}>
        {actions.length > 0 ? (
          <ol className="diagnosis-bullet-list">
            {actions.map((action, index) => (
              <li key={index}>
                {typeof action === "string"
                  ? action
                  : action.description ||
                    action.action ||
                    JSON.stringify(action)}
              </li>
            ))}
          </ol>
        ) : (
          <p className="diagnosis-empty">
            No recommended actions available.
          </p>
        )}
      </Section>

      {/* Evidence Sources */}
      <Section title="Evidence Sources" icon={Database}>
        <div className="diagnosis-source-tags">
          {sources.length > 0 ? (
            sources.map((source, index) => (
              <span key={index}>
                {typeof source === "string"
                  ? source
                  : source.name || JSON.stringify(source)}
              </span>
            ))
          ) : (
            <p className="diagnosis-empty">
              No evidence sources available.
            </p>
          )}
        </div>
      </Section>

      {/* Limitations */}
      <Section title="Investigation Limitations" icon={AlertTriangle}>
        {limitations.length > 0 ? (
          <ul className="diagnosis-bullet-list">
            {limitations.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        ) : (
          <p className="diagnosis-empty">
            No limitations reported.
          </p>
        )}
      </Section>

      {/* Safety */}
      <div className="diagnosis-safety-notice">
        <ShieldCheck size={22} />

        <div>
          <strong>Human Approval Required</strong>

          <p>
            Automatic configuration changes are{" "}
            {investigation.automatic_configuration_changes === false
              ? "disabled"
              : "not confirmed"}.
            Human approval is{" "}
            {investigation.human_approval_required
              ? "required before configuration changes."
              : "not currently marked as required."}
          </p>
        </div>
      </div>

    </div>
  );
}
