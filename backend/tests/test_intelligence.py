
from backend.intelligence.autonomous_investigator import AutonomousInvestigator
from backend.intelligence.root_cause_engine import RootCauseEngine
from backend.remediation.action_planner import ActionPlanner
from backend.learning.incident_memory import IncidentMemory
from backend.learning.pattern_detector import PatternDetector


def test_investigator():
    telemetry = {
        "latency": 180,
        "packet_loss": 7,
        "jitter": 45,
        "cpu_usage": 92,
        "memory_usage": 65
    }

    investigator = AutonomousInvestigator()
    result = investigator.investigate(telemetry)

    assert result["investigation_status"] == "completed"
    assert result["root_cause_analysis"]["status"] == "candidate_found"
    assert result["human_approval_required"] is True

    print("Investigation test passed.")


def test_action_planner():
    engine = RootCauseEngine()

    cause = engine.analyze({
        "latency": 180,
        "packet_loss": 7
    })

    planner = ActionPlanner()
    result = planner.create_plan(cause)

    assert result["requires_human_approval"] is True

    print("Action planner test passed.")


def test_incident_memory():
    memory = IncidentMemory()

    memory.save({
        "root_cause_analysis": {
            "primary_cause": {
                "cause": "Possible network congestion or routing delay"
            }
        }
    })

    detector = PatternDetector()
    result = detector.analyze(memory.get_all())

    assert result["total_incidents_analyzed"] == 1

    print("Incident memory test passed.")


if __name__ == "__main__":
    test_investigator()
    test_action_planner()
    test_incident_memory()

    print("\nAll tests passed.")
