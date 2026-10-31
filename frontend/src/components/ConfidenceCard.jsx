
import React from "react";
import {
  Gauge,
  CheckCircle2,
  AlertTriangle,
  Database,
  Info,
} from "lucide-react";

const ConfidenceCard = ({ confidence = {} }) => {
  const score = Number(confidence.score) || 0;
  const completeness = Number(confidence.completeness) || 0;

  const availableMetrics = confidence.available_metrics || [];
  const missingMetrics = confidence.missing_metrics || [];

  const getScoreLabel = () => {
    if (score >= 80) return "High Evidence Coverage";
    if (score >= 60) return "Moderate Evidence Coverage";
    return "Low Evidence Coverage";
  };

  const getMetricName = (metric) =>
    String(metric).replaceAll("_", " ");

  return (
    <div className="confidence-card">
      <div className="confidence-card-header">
        <div className="confidence-card-title">
          <Gauge size={20} />
          <div>
            <h3>Evidence Coverage</h3>
            <p>Availability of network diagnostic evidence</p>
          </div>
        </div>

        <span className="confidence-label">
          {getScoreLabel()}
        </span>
      </div>

      <div className="confidence-score-area">
        <div className="confidence-score">
          <strong>{score}%</strong>
          <span>Evidence Score</span>
        </div>

        <div className="confidence-completeness">
          <strong>{completeness}%</strong>
          <span>Data Completeness</span>
        </div>
      </div>

      <div className="confidence-progress-section">
        <div className="confidence-progress-heading">
          <span>Evidence Coverage</span>
          <strong>{score}%</strong>
        </div>

        <div className="confidence-progress-track">
          <div
            className="confidence-progress-fill"
            style={{
              width: `${Math.min(100, Math.max(0, score))}%`,
            }}
          />
        </div>

        <div className="confidence-progress-heading">
          <span>Metric Completeness</span>
          <strong>{completeness}%</strong>
        </div>

        <div className="confidence-progress-track">
          <div
            className="confidence-progress-fill completeness"
            style={{
              width: `${Math.min(100, Math.max(0, completeness))}%`,
            }}
          />
        </div>
      </div>

      <div className="confidence-metrics">
        <div className="confidence-metric-group">
          <div className="confidence-metric-heading">
            <CheckCircle2 size={17} />
            <strong>Available Metrics</strong>
            <span>{availableMetrics.length}</span>
          </div>

          <div className="confidence-metric-tags">
            {availableMetrics.length > 0 ? (
              availableMetrics.map((metric) => (
                <span key={metric}>
                  {getMetricName(metric)}
                </span>
              ))
            ) : (
              <small>No available metrics</small>
            )}
          </div>
        </div>

        <div className="confidence-metric-group missing">
          <div className="confidence-metric-heading">
            <AlertTriangle size={17} />
            <strong>Missing Metrics</strong>
            <span>{missingMetrics.length}</span>
          </div>

          <div className="confidence-metric-tags">
            {missingMetrics.length > 0 ? (
              missingMetrics.map((metric) => (
                <span key={metric}>
                  {getMetricName(metric)}
                </span>
              ))
            ) : (
              <small>No missing metrics</small>
            )}
          </div>
        </div>
      </div>

      <div className="confidence-interpretation">
        <Database size={18} />

        <div>
          <strong>Interpretation</strong>
          <p>
            {confidence.interpretation ||
              "No confidence interpretation available."}
          </p>
        </div>
      </div>

      <div className="confidence-note">
        <Info size={16} />
        <p>
          {confidence.note ||
            "Evidence coverage is not a calibrated probability of diagnosis correctness."}
        </p>
      </div>
    </div>
  );
};

export default ConfidenceCard;
