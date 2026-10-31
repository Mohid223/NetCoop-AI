"""CLI entry point. Run from project root:
   python -m backend.main backend/data/scenarios/link_congestion.json
"""
import json
import sys
import os
from backend.core.orchestrator import Orchestrator


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m backend.main <path-to-scenario.json>")
        print("Example: python -m backend.main backend/data/scenarios/link_congestion.json")
        sys.exit(1)

    path = sys.argv[1]

    if not os.path.exists(path):
        print(f"Error: File not found → {path}")
        sys.exit(1)

    with open(path) as f:
        scenario = json.load(f)

    print(f"\n>>> Running diagnosis for: {path}\n")

    orch = Orchestrator()
    result = orch.run(scenario)

    # Save message log
    os.makedirs("backend/outputs", exist_ok=True)
    output_path = f"backend/outputs/{result['incident_id']}_messages.json"
    
    with open(output_path, "w") as f:
        json.dump(result["message_log"], f, indent=2)

    print(f"\n>>> Total messages exchanged: {len(result['message_log'])}")
    print(f">>> Message log saved to: {output_path}")


if __name__ == "__main__":
    main()