
import json
from pathlib import Path

import pytest

from backend.core.orchestrator import Orchestrator


SCENARIO_DIR = Path(__file__).resolve().parents[1] / "data" / "scenarios"


@pytest.mark.parametrize(
    "filename, expected_status",
    [
        ("normal.json", "healthy"),
        ("link_congestion.json", "diagnosed"),
        ("weak_wifi.json", "diagnosed"),
        ("ethernet_fault.json", "diagnosed"),
        ("dns_failure.json", "diagnosed"),
        ("dhcp_failure.json", "diagnosed"),
        ("malformed.json", "insufficient_evidence"),
    ],
)
def test_scenario_diagnosis(filename, expected_status):
    scenario_path = SCENARIO_DIR / filename

    with scenario_path.open("r", encoding="utf-8-sig") as file:
        scenario = json.load(file)

    orchestrator = Orchestrator()
    result = orchestrator.run(scenario)

    assert "report" in result
    assert isinstance(result["report"], dict)
    assert result["report"]["status"] == expected_status
    assert result["incident_id"] == scenario["incident_id"]


def test_invalid_scenario_rejected():
    orchestrator = Orchestrator()

    with pytest.raises(ValueError):
        orchestrator.run("not a JSON object")


def test_message_log_is_returned():
    scenario = {
        "incident_id": "TEST-001",
        "telemetry": {
            "latency_ms": 20,
            "jitter_ms": 2,
            "packet_loss_pct": 0.1,
        },
        "devices": [],
        "wifi": {},
        "dns": {},
        "dhcp": {},
    }

    result = Orchestrator().run(scenario)

    assert isinstance(result["message_log"], list)
    assert len(result["message_log"]) > 0
