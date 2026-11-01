
"""Produces the final structured JSON diagnostic report."""

import json
import os

from backend.agents.base_agent import BaseAgent
from backend.core.schema import MsgType


class ReportingAgent(BaseAgent):
    name = "reporting_agent"

    def __init__(self, bus, output_dir="backend/outputs"):
        super().__init__(bus)
        self.output_dir = output_dir
        self.final_report = None

    def handle(self, message):
        if message.msg_type != MsgType.RESULT:
            return

        payload = message.payload

        # Preserve actions from FaultCorrelationAgent.
        # Use fallback recommendations only if none were provided.
        actions = payload.get("recommended_actions")

        if not isinstance(actions, list) or not actions:
            actions = self._recommend(
                payload.get("suspected_root_cause", "")
            )

        report = {
            "incident_id": message.incident_id,
            "status": payload.get("status", "insufficient_evidence"),
            "suspected_root_cause": payload.get(
                "suspected_root_cause", "Unknown"
            ),
            "confidence": payload.get("confidence", 0.0),
            "affected_devices": payload.get("affected_devices", []),
            "supporting_evidence": payload.get(
                "supporting_evidence", []
            ),
            "alternative_causes": payload.get(
                "alternative_causes", []
            ),
            "recommended_actions": actions,
            "evidence_sources": payload.get("evidence_sources", []),
            "limitations": payload.get("limitations", []),
        }

        self.final_report = report

        os.makedirs(self.output_dir, exist_ok=True)

        path = os.path.join(
            self.output_dir,
            f"{message.incident_id}_report.json"
        )

        with open(path, "w", encoding="utf-8") as file:
            json.dump(report, file, indent=2)

        print("\n" + "=" * 60)
        print("FINAL DIAGNOSTIC REPORT")
        print("=" * 60)
        print(json.dumps(report, indent=2))
        print("=" * 60 + "\n")

    def _recommend(self, cause: str):
        table = {
            "Link congestion causing egress queue drops": [
                "Inspect upstream and egress link utilization",
                "Review queue configuration and traffic distribution",
                "Consider bandwidth upgrade if persistent"
            ],
            "Weak WiFi signal causing retransmissions": [
                "Reposition or add access points",
                "Check for interference and channel overlap",
                "Verify client device signal strength"
            ],
            "WiFi retransmission storm": [
                "Change WiFi channel to less congested one",
                "Reduce transmit power if too high",
                "Check for hidden node problems"
            ],
            "Ethernet/interface fault": [
                "Test/replace cable and SFP on affected port",
                "Check interface error counters and CRC errors",
                "Verify duplex and speed settings"
            ],
            "Hardware failure / device unreachable": [
                "Verify power and console access",
                "Dispatch on-site inspection",
                "Check upstream switch port status"
            ],
            "Device CPU overload": [
                "Review control-plane processes",
                "Apply Control Plane Policing (CoPP)",
                "Check for routing protocol instability"
            ],
            "Memory pressure on device": [
                "Investigate memory-leaking processes",
                "Consider device reload during maintenance window",
                "Monitor memory trend over time"
            ],
            "High latency — possible congestion": [
                "Check link utilization on the path",
                "Look for microbursts or queue buildup",
                "Verify QoS policies"
            ],
            "Packet loss due to link instability": [
                "Check physical layer (cable, optics, errors)",
                "Inspect interface counters for CRC/input errors",
                "Test with different transceiver if possible"
            ],
        }

        return table.get(cause, [
            "Collect additional telemetry before taking action",
            "Verify the diagnosis with network team"
        ])
