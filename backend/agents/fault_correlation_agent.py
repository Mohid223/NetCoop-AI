
"""The Brain — correlates multi-agent evidence to identify network root causes."""

from backend.agents.base_agent import BaseAgent
from backend.core.schema import MsgType


class FaultCorrelationAgent(BaseAgent):
    name = "fault_correlation_agent"

    RULES = {
        "link_utilization_pct": ("Link congestion causing egress queue drops", 0.90),
        "queue_drops": ("Link congestion causing egress queue drops", 0.88),
        "packet_loss_pct": ("Packet loss due to link instability", 0.78),
        "latency_ms": ("High latency — possible congestion", 0.72),
        "jitter_ms": ("High jitter — network instability", 0.68),
        "weak_wifi_signal": ("Weak WiFi signal causing retransmissions", 0.92),
        "high_retransmission": ("WiFi retransmission storm", 0.85),
        "interface_errors": ("Ethernet/interface fault", 0.90),
        "device_down": ("Hardware failure / device unreachable", 0.95),
        "cpu_utilization_pct": ("Device CPU overload", 0.82),
        "memory_utilization_pct": ("Memory pressure on device", 0.78),
        "dns_failure": ("DNS resolution failure", 0.92),
        "dns_resolution_failure": ("DNS resolution failure", 0.92),
        "dhcp_failure": ("DHCP service or address assignment failure", 0.92),
        "dhcp_lease_failure": ("DHCP service or address assignment failure", 0.90),
        "schema_mismatch": ("Agent interoperability or schema mismatch", 0.90),
        "missing_fields": ("Incomplete telemetry data", 0.70),
    }

    ACTIONS = {
        "Link congestion causing egress queue drops": [
            "Inspect link utilization and egress queue drops.",
            "Check bandwidth capacity and traffic distribution.",
            "Consider traffic shaping or additional bandwidth."
        ],
        "Packet loss due to link instability": [
            "Inspect packet loss across affected network links.",
            "Check physical connections and network device logs."
        ],
        "High latency — possible congestion": [
            "Measure latency across network paths.",
            "Inspect link utilization and routing performance."
        ],
        "High jitter — network instability": [
            "Investigate unstable network paths.",
            "Check congestion and packet scheduling."
        ],
        "Weak WiFi signal causing retransmissions": [
            "Check WiFi signal strength in affected areas.",
            "Inspect access point placement and interference."
        ],
        "WiFi retransmission storm": [
            "Inspect WiFi retransmission rates.",
            "Check wireless interference and access point health."
        ],
        "Ethernet/interface fault": [
            "Inspect interface error counters.",
            "Check cables, ports and interface status."
        ],
        "Hardware failure / device unreachable": [
            "Verify device power and connectivity.",
            "Inspect device health and availability."
        ],
        "Device CPU overload": [
            "Inspect CPU-intensive processes.",
            "Check device workload and resource utilization."
        ],
        "Memory pressure on device": [
            "Inspect memory utilization.",
            "Check for memory-intensive processes."
        ],
        "DNS resolution failure": [
            "Verify DNS server availability.",
            "Test DNS resolution and inspect DNS configuration."
        ],
        "DHCP service or address assignment failure": [
            "Check DHCP server availability.",
            "Inspect address pools and lease assignment."
        ],
        "Agent interoperability or schema mismatch": [
            "Verify protocol and schema versions.",
            "Check field names, data types and measurement units."
        ],
        "Incomplete telemetry data": [
            "Collect the missing telemetry fields.",
            "Verify the data source and agent configuration."
        ],
    }

    def __init__(self, bus):
        super().__init__(bus)
        self.findings = {}
        self.errors = []
        self.responders = set()
        self.incident_id = None
        self.expected = 3
        self.completed = False

    def handle(self, message):
        if message.msg_type == MsgType.REQUEST:
            self.incident_id = message.incident_id
            self.findings = {}
            self.errors = []
            self.responders = set()
            self.completed = False

            expected = message.payload.get("expected_agents", 3)

            if isinstance(expected, int) and not isinstance(expected, bool):
                self.expected = max(1, expected)
            else:
                self.expected = 3

            return

        if message.incident_id != self.incident_id or self.completed:
            return

        if message.msg_type == MsgType.ERROR:
            if message.sender in self.responders:
                return

            self.errors.append({
                "agent": message.sender,
                "details": message.payload
            })
            self.responders.add(message.sender)
            self._check_completion()
            return

        if message.msg_type == MsgType.FINDING:
            if message.sender in self.responders:
                return

            self.findings[message.sender] = message
            self.responders.add(message.sender)
            self._check_completion()

    def _check_completion(self):
        if len(self.responders) >= self.expected:
            self.correlate()

    def correlate(self):
        if self.completed:
            return

        self.completed = True

        anomaly_sources = {}
        all_evidence = []
        all_devices = set()
        sources = []

        for sender, msg in self.findings.items():
            sources.append(sender)
            payload = msg.payload

            if not isinstance(payload, dict):
                continue

            anomalies = payload.get("anomalies", [])

            if isinstance(anomalies, list):
                for anomaly in set(
                    a for a in anomalies if isinstance(a, str)
                ):
                    anomaly_sources.setdefault(anomaly, set()).add(sender)

            evidence = payload.get("evidence", [])

            if isinstance(evidence, list):
                all_evidence.extend(
                    item for item in evidence
                    if isinstance(item, (str, dict))
                )

            devices = payload.get("affected_devices", [])

            if isinstance(devices, list):
                all_devices.update(
                    device for device in devices
                    if isinstance(device, str)
                )

        # Healthy: every expected agent responded successfully,
        # with no errors and no reported anomalies.
        if (
            len(self.responders) >= self.expected
            and len(self.findings) >= self.expected
            and not self.errors
            and not anomaly_sources
        ):
            self._send_report({
                "status": "healthy",
                "suspected_root_cause": "No network fault detected",
                "confidence": 0.90,
                "affected_devices": sorted(all_devices),
                "supporting_evidence": all_evidence,
                "alternative_causes": [],
                "recommended_actions": [
                    "Continue monitoring network performance.",
                    "Maintain regular infrastructure health checks."
                ],
                "evidence_sources": sources,
                "limitations": [
                    "Healthy status is based on the telemetry provided by the responding agents."
                ]
            })
            return

        # Calculate root-cause heuristic scores.
        scores = {}

        wifi_signatures = {
            "weak_wifi_signal",
            "high_retransmission",
        }

        generic_symptoms = {
            "packet_loss_pct",
            "latency_ms",
            "jitter_ms",
        }

        has_weak_wifi_signal = "weak_wifi_signal" in anomaly_sources
        has_wifi_signature = bool(
            wifi_signatures.intersection(anomaly_sources)
        )

        supporting_wifi_symptoms = (
            generic_symptoms.intersection(anomaly_sources)
            if has_wifi_signature else set()
        )

        for anomaly, agents in anomaly_sources.items():
            rule = self.RULES.get(anomaly)

            if rule is None:
                continue

            cause, weight = rule

            # High retransmission alone is not proof of weak signal.
            if anomaly == "high_retransmission" and has_weak_wifi_signal:
                cause = "Weak WiFi signal causing retransmissions"

            if has_wifi_signature and anomaly in generic_symptoms:
                continue

            contribution = weight * len(agents)
            scores[cause] = scores.get(cause, 0) + contribution

        if has_wifi_signature and has_weak_wifi_signal:
            wifi_cause = "Weak WiFi signal causing retransmissions"
            scores[wifi_cause] = scores.get(wifi_cause, 0) + (
                0.10 * len(supporting_wifi_symptoms)
            )

        # No recognized root cause.
        if not scores:
            limitations = [
                "No recognized root-cause anomaly was found.",
                "Additional telemetry is required for reliable diagnosis."
            ]

            if self.errors:
                limitations.append(
                    "One or more agents reported errors."
                )

            self._send_report({
                "status": "insufficient_evidence",
                "suspected_root_cause": (
                    "Unable to determine root cause with available evidence"
                ),
                "confidence": 0.0,
                "affected_devices": sorted(all_devices),
                "supporting_evidence": all_evidence,
                "alternative_causes": [],
                "recommended_actions": [
                    "Collect additional network telemetry.",
                    "Check agents that reported errors."
                ],
                "evidence_sources": sources,
                "limitations": limitations
            })
            return

        ranked = sorted(
            scores.items(),
            key=lambda item: item[1],
            reverse=True
        )

        top_cause, top_score = ranked[0]

        # Heuristic score, NOT a calibrated probability.
        confidence = round(
            min(0.95, top_score / (top_score + 0.75)),
            2
        )

        alternatives = [
            cause for cause, _ in ranked[1:4]
        ]

        limitations = []

        if confidence <= 0.70:
            limitations.append(
                "Heuristic confidence is low; additional telemetry is recommended."
            )

        if len(self.findings) < self.expected:
            limitations.append(
                "Not all expected agents provided findings."
            )

        if self.errors:
            limitations.append(
                "One or more agents reported errors; diagnosis may be incomplete."
            )

        self._send_report({
            "status": "diagnosed",
            "suspected_root_cause": top_cause,
            "confidence": confidence,
            "affected_devices": sorted(all_devices),
            "supporting_evidence": all_evidence,
            "alternative_causes": alternatives,
            "recommended_actions": self.ACTIONS.get(
                top_cause,
                ["Collect more evidence before taking corrective action."]
            ),
            "evidence_sources": sources,
            "limitations": limitations
        })

    def _send_report(self, report):
        self.send(
            "reporting_agent",
            MsgType.RESULT,
            self.incident_id,
            report
        )
