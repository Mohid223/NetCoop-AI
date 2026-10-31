"""Orchestrator — wires all agents and runs a complete diagnosis."""
import uuid
from backend.core.message_bus import MessageBus
from backend.core.schema import Message, MsgType
from backend.agents.telemetry_agent import TelemetryAgent
from backend.agents.infrastructure_agent import InfrastructureAgent
from backend.agents.connectivity_agent import ConnectivityAgent
from backend.agents.fault_correlation_agent import FaultCorrelationAgent
from backend.agents.reporting_agent import ReportingAgent


class Orchestrator:
    def __init__(self):
        self.bus = MessageBus()

        # Initialize all agents
        self.perf = TelemetryAgent(self.bus)
        self.infra = InfrastructureAgent(self.bus)
        self.conn = ConnectivityAgent(self.bus)
        self.corr = FaultCorrelationAgent(self.bus)
        self.rep = ReportingAgent(self.bus)

    def run(self, scenario: dict) -> dict:
        incident_id = scenario.get("incident_id") or f"INC-{uuid.uuid4().hex[:6].upper()}"

        # 1. Inform Correlation Agent how many findings to expect
        self.bus.publish(
            Message(
                sender="orchestrator",
                recipient="fault_correlation_agent",
                msg_type=MsgType.REQUEST,
                incident_id=incident_id,
                payload={"expected_agents": 3},
            )
        )

        # 2. Send data to specialized agents
        self.bus.publish(
            Message(
                sender="orchestrator",
                recipient="performance_agent",
                msg_type=MsgType.REQUEST,
                incident_id=incident_id,
                payload={"telemetry": scenario.get("telemetry", {})},
            )
        )

        self.bus.publish(
            Message(
                sender="orchestrator",
                recipient="infrastructure_agent",
                msg_type=MsgType.REQUEST,
                incident_id=incident_id,
                payload={"devices": scenario.get("devices", [])},
            )
        )

        self.bus.publish(
            Message(
                sender="orchestrator",
                recipient="connectivity_agent",
                msg_type=MsgType.REQUEST,
                incident_id=incident_id,
                payload={
                    "wifi": scenario.get("wifi", {}),
                    "devices": scenario.get("devices", []),
                },
            )
        )

        return {
            "incident_id": incident_id,
            "report": self.rep.final_report,
            "message_log": self.bus.get_log(),
        }