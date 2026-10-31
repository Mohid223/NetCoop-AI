import os
import sys
import json
import pytest

# --- FIX: Add project root to sys.path so 'backend' can be imported ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)
# -----------------------------------------------------------------------

from backend.core.orchestrator import Orchestrator

# Path setup
SCENARIO_DIR = os.path.join(ROOT_DIR, "backend", "data", "scenarios")

def run_scenario(filename):
    with open(os.path.join(SCENARIO_DIR, filename)) as f:
        scenario = json.load(f)
    orch = Orchestrator()
    return orch.run(scenario)

def test_link_congestion():
    """Ensure link congestion is correctly identified."""
    result = run_scenario("link_congestion.json")
    report = result["report"]
    assert report["status"] == "diagnosed"
    assert "Link congestion" in report["suspected_root_cause"]
    assert report["confidence"] > 0.8

def test_weak_wifi():
    """Ensure weak WiFi is correctly identified."""
    result = run_scenario("weak_wifi.json")
    report = result["report"]
    assert "WiFi" in report["suspected_root_cause"]
    assert report["confidence"] > 0.8

def test_malformed():
    """Ensure system does not crash on bad data and diagnoses what it can."""
    result = run_scenario("malformed.json")
    report = result["report"]
    # System should handle "HIGH", None, "N/A", "weak" without crashing
    assert report is not None
    assert "Hardware failure" in report["suspected_root_cause"]

def test_normal():
    """Ensure healthy network does not trigger a false alarm."""
    result = run_scenario("normal.json")
    report = result["report"]
    assert report["status"] == "insufficient_evidence"
    assert report["confidence"] == 0.0