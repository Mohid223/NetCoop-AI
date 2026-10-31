from .root_cause_engine import RootCauseEngine
from .causal_graph import CausalGraph
from .decision_engine import DecisionEngine
from .confidence_engine import ConfidenceEngine
from .telemetry_normalizer import normalize_telemetry

# from diagnostics.diagnostic_runner import DiagnosticRunner
from backend.diagnostics.diagnostic_runner import DiagnosticRunner

class AutonomousInvestigator:

    def __init__(self):
        self.root_cause_engine = RootCauseEngine()
        self.causal_graph = CausalGraph()
        self.decision_engine = DecisionEngine()
        self.confidence_engine = ConfidenceEngine()
        self.diagnostic_runner = DiagnosticRunner()

    def investigate(
        self,
        telemetry: dict,
        execute_diagnostics=False,
        host="8.8.8.8"
    ):
        if not isinstance(telemetry, dict):
            raise ValueError("Telemetry must be a dictionary")

        normalized = normalize_telemetry(telemetry)
        diagnostic_results = []

        # Run real diagnostic tests only when requested.
        if execute_diagnostics:
            diagnostic_results = self.diagnostic_runner.run_all(host=host)

            for result in diagnostic_results:
                if result.get("test") == "latency":
                    value = result.get("average_latency_ms")
                    if value is not None:
                        normalized["latency"] = value

                elif result.get("test") == "packet_loss":
                    value = result.get("packet_loss_percent")
                    if value is not None:
                        normalized["packet_loss"] = value

                elif result.get("test") == "dns_resolution":
                    normalized["dns_status"] = (
                        "healthy" if result.get("success") else "failed"
                    )

        # Analyze the combined telemetry.
        root_cause = self.root_cause_engine.analyze(normalized)

        diagnostic_plan = self.decision_engine.create_plan(
            root_cause,
            normalized
        )

        graph = self.causal_graph.build_from_findings(
            root_cause.get("candidates", [])
        )

        confidence = self.confidence_engine.calculate(
            normalized,
            evidence_count=len(root_cause.get("candidates", []))
        )

        return {
            "investigation_status": "completed",
            "mode": "autonomous",
            "normalized_telemetry": normalized,
            "diagnostic_results": diagnostic_results,
            "root_cause_analysis": root_cause,
            "causal_graph": graph,
            "diagnostic_plan": diagnostic_plan,
            "confidence": confidence,
            "human_approval_required": True,
            "automatic_configuration_changes": False
        }