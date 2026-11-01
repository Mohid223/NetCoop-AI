
"""Analyzes device health and Ethernet/interface faults."""

from backend.agents.base_agent import BaseAgent
from backend.core.schema import MsgType


class InfrastructureAgent(BaseAgent):
    name = "infrastructure_agent"

    THRESHOLDS = {
        "cpu_utilization_pct": 85.0,
        "memory_utilization_pct": 85.0,
        "queue_drops": 50.0,
        "interface_errors": 10.0,
        "crc_errors": 10.0,
        "input_errors": 10.0,
        "output_errors": 10.0,
    }

    def handle(self, message):
        if message.msg_type != MsgType.REQUEST:
            return

        devices = message.payload.get("devices", [])
        incident_id = message.incident_id

        if not isinstance(devices, list) or not devices:
            self.send(
                "fault_correlation_agent",
                MsgType.ERROR,
                incident_id,
                {"error": "No valid device data", "agent": self.name},
            )
            return

        findings = []
        evidence = []
        affected = []

        def mark_affected(device_id):
            if device_id not in affected:
                affected.append(device_id)

        for dev in devices:
            if not isinstance(dev, dict):
                continue

            dev_id = dev.get("device_id", "UNKNOWN")

            # Device availability
            status = str(dev.get("status", "")).strip().lower()

            if status in ("down", "offline", "unreachable"):
                findings.append("device_down")
                mark_affected(dev_id)
                evidence.append({
                    "device": dev_id,
                    "metric": "status",
                    "value": status,
                    "interpretation": f"{dev_id} is down or unreachable",
                })

            # Ethernet link state
            link_state = str(
                dev.get("link_state", dev.get("interface_status", ""))
            ).strip().lower()

            if link_state in ("down", "failed", "not_connected"):
                findings.append("interface_errors")
                mark_affected(dev_id)
                evidence.append({
                    "device": dev_id,
                    "metric": "link_state",
                    "value": link_state,
                    "interpretation": f"Ethernet interface on {dev_id} is down",
                })

            # Device performance and interface counters
            for metric, threshold in self.THRESHOLDS.items():
                value = dev.get(metric)

                if value is None:
                    continue

                try:
                    if isinstance(value, bool):
                        raise ValueError("Boolean is not a numeric metric")
                    value = float(value)

                    if value < 0:
                        raise ValueError("Metric cannot be negative")

                except (TypeError, ValueError):
                    self.send(
                        "fault_correlation_agent",
                        MsgType.ERROR,
                        incident_id,
                        {
                            "error": f"Invalid {metric} on {dev_id}",
                            "agent": self.name,
                        },
                    )
                    continue

                if value > threshold:
                    anomaly = (
                        "interface_errors"
                        if metric in (
                            "interface_errors",
                            "crc_errors",
                            "input_errors",
                            "output_errors",
                        )
                        else metric
                    )

                    findings.append(anomaly)
                    mark_affected(dev_id)

                    evidence.append({
                        "device": dev_id,
                        "metric": metric,
                        "value": value,
                        "interpretation": (
                            f"{metric} exceeds threshold of {threshold} "
                            f"on {dev_id}"
                        ),
                    })

        confidence = min(1.0, len(set(findings)) / 3.0) if findings else 0.1

        self.send(
            recipient="fault_correlation_agent",
            msg_type=MsgType.FINDING,
            incident_id=incident_id,
            payload={
                "agent": self.name,
                "anomalies": sorted(set(findings)),
                "evidence": evidence,
                "affected_devices": affected,
            },
            confidence=confidence,
        )
