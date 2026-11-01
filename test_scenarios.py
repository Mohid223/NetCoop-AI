import json
from pathlib import Path
from backend.core.orchestrator import Orchestrator

folder = Path("backend/data/scenarios")

for file in sorted(folder.glob("*.json")):
    scenario = json.loads(file.read_text(encoding="utf-8-sig"))
    result = Orchestrator().run(scenario)["report"]
    print(file.name, "->", result["status"], "|", result["suspected_root_cause"])
