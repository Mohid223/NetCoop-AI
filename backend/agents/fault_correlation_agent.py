"""The Brain — combines evidence from all agents to find root cause."""
from backend.agents.base_agent import BaseAgent
from backend.core.schema import MsgType


class FaultCorrelationAgent(BaseAgent):
    name = "fault_correlation_agent"

    # Weighted rule table: anomaly → (root cause, base confidence)
    RULES = {
        "link_utilization_pct":     ("Link congestion causing egress queue drops", 0.90),
        "queue_drops":              ("Link congestion causing egress queue drops", 0.88),
        "packet_loss_pct":          ("Packet loss due to link instability", 0.78),
        "latency_ms":               ("High latency — possible congestion", 0.72),
        "jitter_ms":                ("High jitter — network instability", 0.68),
        "weak_wifi_signal":         ("Weak WiFi signal causing retransmissions", 0.92),
        "high_retransmission":      ("WiFi retransmission storm", 0.85),
        "interface_errors":         ("Ethernet/interface fault", 0.90),
        "device_down":              ("Hardware failure / device unreachable", 0.95),
        "cpu_utilization_pct":      ("Device CPU overload", 0.82),
        "memory_utilization_pct":   ("Memory pressure on device", 0.78),
    }

    def __init__(self, bus):
        super().__init__(bus)
        self.findings = {}
        self.incident_id = None
        self.expected = 3

    def handle(self, message):
        if message.msg_type == MsgType.REQUEST:
            self.incident_id = message.incident_id
            self.findings = {}
            self.expected = message.payload.get("expected_agents", 3)
            return

        if message.msg_type == MsgType.ERROR:
            self.findings.setdefault("errors", []).append(message.payload)
            return

        if message.msg_type == MsgType.FINDING:
            self.findings[message.sender] = message
            finding_count = sum(1 for k in self.findings if k != "errors")

            if finding_count >= self.expected:
                self.correlate()

    def correlate(self):
        all_anomalies = {}
        all_evidence = []
        all_devices = set()
        sources = []

        for sender, msg in self.findings.items():
            if sender == "errors":
                continue

            sources.append(sender)
            payload = msg.payload

            for anomaly in payload.get("anomalies", []):
                all_anomalies[anomaly] = all_anomalies.get(anomaly, 0) + 1

            all_evidence.extend(payload.get("evidence", []))
            all_devices.update(payload.get("affected_devices", []))

        # Score each possible root cause
        scores = {}
        for anomaly, count in all_anomalies.items():
            if anomaly in self.RULES:
                cause, base_conf = self.RULES[anomaly]
                scores[cause] = scores.get(cause, 0) + (base_conf * count)

        # No strong evidence found
        if not scores:
            self.send(
                "reporting_agent",
                MsgType.RESULT,
                self.incident_id,
                {
                    "status": "insufficient_evidence",
                    "suspected_root_cause": "Unable to determine root cause with available evidence",
                    "confidence": 0.0,
                    "affected_devices": sorted(list(all_devices)),
                    "supporting_evidence": all_evidence,
                    "alternative_causes": [],
                    "evidence_sources": sources,
                    "limitations": [
                        "Not enough correlated anomalies from agents",
                        "More telemetry data is required for reliable diagnosis"
                    ],
                },
            )
            return

        # Rank causes
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_cause, top_score = ranked[0]
        total_score = sum(score for _, score in ranked)

        # Confidence calculation (safe & logical)
        confidence = round(min(top_score / total_score, 0.99), 2)

        # Boost confidence if multiple different anomalies support the same cause
        supporting_anomalies = sum(
            1 for a in all_anomalies if self.RULES.get(a, (None,))[0] == top_cause
        )
        if supporting_anomalies >= 2:
            confidence = min(0.99, confidence + 0.06)

        alternatives = [cause for cause, _ in ranked[1:3]]

        limitations = []
        if confidence < 0.70:
            limitations.append("Low confidence — additional telemetry recommended")
        if len(sources) < 3:
            limitations.append("Not all agents contributed evidence")

        self.send(
            "reporting_agent",
            MsgType.RESULT,
            self.incident_id,
            {
                "status": "diagnosed",
                "suspected_root_cause": top_cause,
                "confidence": confidence,
                "affected_devices": sorted(list(all_devices)),
                "supporting_evidence": all_evidence,
                "alternative_causes": alternatives,
                "evidence_sources": sources,
                "limitations": limitations,
            },
        )