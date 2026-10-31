"""Analyzes device health: CPU, memory, queue drops, interface errors, status."""
from backend.agents.base_agent import BaseAgent
from backend.core.schema import MsgType


class InfrastructureAgent(BaseAgent):
    name = "infrastructure_agent"

    THRESHOLDS = {
        "cpu_utilization_pct": 85.0,
        "memory_utilization_pct": 85.0,
        "queue_drops": 50.0,
        "interface_errors": 10.0,
    }

    def handle(self, message):
        if message.msg_type != MsgType.REQUEST:
            return

        devices = message.payload.get("devices", [])
        incident_id = message.incident_id

        if not devices:
            self.send(
                "fault_correlation_agent",
                MsgType.ERROR,
                incident_id,
                {"error": "no device data", "agent": self.name},
            )
            return

        findings = []
        evidence = []
        affected = []

        for dev in devices:
            if not isinstance(dev, dict):
                continue

            dev_id = dev.get("device_id", "UNKNOWN")

            # Check status
            status = str(dev.get("status", "")).lower()
            if status == "down":
                findings.append("device_down")
                if dev_id not in affected:
                    affected.append(dev_id)
                evidence.append({
                    "device": dev_id,
                    "metric": "status",
                    "value": "down",
                    "interpretation": f"{dev_id} is unreachable / down",
                })

            # Check metrics
            for metric, threshold in self.THRESHOLDS.items():
                val = dev.get(metric)
                if val is None:
                    continue

                try:
                    val = float(val)
                except (TypeError, ValueError):
                    self.send(
                        "fault_correlation_agent",
                        MsgType.ERROR,
                        incident_id,
                        {"error": f"bad {metric} on {dev_id}: {val!r}"},
                    )
                    continue

                if val > threshold:
                    findings.append(metric)
                    if dev_id not in affected:
                        affected.append(dev_id)
                    evidence.append({
                        "device": dev_id,
                        "metric": metric,
                        "value": val,
                        "interpretation": f"{metric} is critical on {dev_id} (>{threshold})",
                    })

        confidence = min(1.0, len(findings) / 3.0) if findings else 0.1

        self.send(
            recipient="fault_correlation_agent",
            msg_type=MsgType.FINDING,
            incident_id=incident_id,
            payload={
                "agent": self.name,
                "anomalies": findings,
                "evidence": evidence,
                "affected_devices": affected,
            },
            confidence=confidence,
        )