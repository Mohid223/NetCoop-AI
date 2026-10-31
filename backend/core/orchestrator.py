"""Orchestrator for multi-agent and autonomous network diagnosis."""

import uuid

from backend.core.message_bus import MessageBus
from backend.core.schema import Message, MsgType
from backend.agents.telemetry_agent import TelemetryAgent
from backend.agents.infrastructure_agent import InfrastructureAgent
from backend.agents.connectivity_agent import ConnectivityAgent
from backend.agents.fault_correlation_agent import FaultCorrelationAgent
from backend.agents.reporting_agent import ReportingAgent
from backend.intelligence.autonomous_investigator import AutonomousInvestigator


class Orchestrator:

    def __init__(self):
        self.bus = MessageBus()

        self.perf = TelemetryAgent(self.bus)
        self.infra = InfrastructureAgent(self.bus)
        self.conn = ConnectivityAgent(self.bus)
        self.corr = FaultCorrelationAgent(self.bus)
        self.rep = ReportingAgent(self.bus)

        self.investigator = AutonomousInvestigator()

    def run(self, scenario: dict) -> dict:
        incident_id = scenario.get(
            "incident_id",
            f"INC-{uuid.uuid4().hex[:6].upper()}"
        )

        self.bus.publish(Message(
            sender="orchestrator",
            recipient="fault_correlation_agent",
            msg_type=MsgType.REQUEST,
            incident_id=incident_id,
            payload={"expected_agents": 3},
        ))

        self.bus.publish(Message(
            sender="orchestrator",
            recipient="performance_agent",
            msg_type=MsgType.REQUEST,
            incident_id=incident_id,
            payload={"telemetry": scenario.get("telemetry", {})},
        ))

        self.bus.publish(Message(
            sender="orchestrator",
            recipient="infrastructure_agent",
            msg_type=MsgType.REQUEST,
            incident_id=incident_id,
            payload={"devices": scenario.get("devices", [])},
        ))

        self.bus.publish(Message(
            sender="orchestrator",
            recipient="connectivity_agent",
            msg_type=MsgType.REQUEST,
            incident_id=incident_id,
            payload={
                "wifi": scenario.get("wifi", {}),
                "devices": scenario.get("devices", []),
            },
        ))

        # Combine telemetry and device metrics for investigation.
        telemetry = dict(scenario.get("telemetry", {}))
        devices = scenario.get("devices", [])

        if devices:
            device = devices[0]
            telemetry.setdefault(
                "cpu_utilization_pct",
                device.get("cpu_utilization_pct")
            )
            telemetry.setdefault(
                "memory_utilization_pct",
                device.get("memory_utilization_pct")
            )

        investigation = self.investigator.investigate(
            telemetry,
            execute_diagnostics=scenario.get("run_diagnostics", False),
            host=scenario.get("target_host", "8.8.8.8")
        )

        return {
            "incident_id": incident_id,
            "report": self.rep.final_report,
            "autonomous_investigation": investigation,
            "message_log": self.bus.get_log(),
        }