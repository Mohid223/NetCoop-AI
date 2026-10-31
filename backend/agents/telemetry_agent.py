"""Analyzes performance telemetry (latency, jitter, packet loss, utilization)."""
from backend.agents.base_agent import BaseAgent
from backend.core.schema import MsgType


class TelemetryAgent(BaseAgent):
    name = "performance_agent"

    THRESHOLDS = {
        "latency_ms": 80.0,
        "jitter_ms": 15.0,
        "packet_loss_pct": 2.0,
        "link_utilization_pct": 80.0,
        "throughput_mbps": None,  # optional
    }

    def handle(self, message):
        if message.msg_type != MsgType.REQUEST:
            return

        telemetry = message.payload.get("telemetry", {})
        incident_id = message.incident_id

        if not telemetry:
            self.send(
                "fault_correlation_agent",
                MsgType.ERROR,
                incident_id,
                {"error": "empty telemetry", "agent": self.name},
            )
            return

        findings = []
        evidence = []

        for metric, threshold in self.THRESHOLDS.items():
            if threshold is None:
                continue

            value = telemetry.get(metric)
            if value is None:
                continue

            try:
                value = float(value)
            except (TypeError, ValueError):
                self.send(
                    "fault_correlation_agent",
                    MsgType.ERROR,
                    incident_id,
                    {"error": f"non-numeric {metric}={value!r}", "agent": self.name},
                )
                continue

            if value > threshold:
                findings.append(metric)
                evidence.append({
                    "metric": metric,
                    "value": value,
                    "interpretation": f"{metric} exceeds threshold of {threshold}",
                })

        confidence = min(1.0, len(findings) / 4.0) if findings else 0.1

        self.send(
            recipient="fault_correlation_agent",
            msg_type=MsgType.FINDING,
            incident_id=incident_id,
            payload={
                "agent": self.name,
                "anomalies": findings,
                "evidence": evidence,
            },
            confidence=confidence,
        )