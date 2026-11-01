import json
from pathlib import Path
from backend.core.orchestrator import Orchestrator

scenario = json.loads(
    Path("backend/data/scenarios/normal.json").read_text(encoding="utf-8-sig")
)

result = Orchestrator().run(scenario)

print("\n--- AGENT MESSAGE LOG ---")
for message in result["message_log"]:
    print(json.dumps(message, indent=2))

print("\n--- FINAL REPORT ---")
print(json.dumps(result["report"], indent=2))
