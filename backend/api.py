"""FastAPI wrapper around the Orchestrator for React frontend."""
import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.core.orchestrator import Orchestrator
from backend.real_collector import run_real_world_diagnosis

app = FastAPI(
    title="NetCoop AI API",
    description="Multi-Agent Network Fault Diagnosis System",
    version="1.0.0"
)

# Allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SCENARIO_DIR = os.path.join(os.path.dirname(__file__), "data", "scenarios")


class RunRequest(BaseModel):
    scenario_file: str


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "NetCoop AI"}


@app.get("/api/scenarios")
def list_scenarios():
    """List all available scenario JSON files."""
    if not os.path.exists(SCENARIO_DIR):
        return {"scenarios": []}
    
    files = sorted([f for f in os.listdir(SCENARIO_DIR) if f.endswith(".json")])
    return {"scenarios": files}


@app.post("/api/run")
def run_diagnosis(req: RunRequest):
    """Run a full diagnosis for a given scenario."""
    path = os.path.join(SCENARIO_DIR, req.scenario_file)
    
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"Scenario '{req.scenario_file}' not found")

    with open(path) as f:
        scenario = json.load(f)

    orch = Orchestrator()
    result = orch.run(scenario)

    # Make sure message_log is fully serializable
    log = []
    for m in result.get("message_log", []):
        m_copy = dict(m)
        if hasattr(m_copy.get("msg_type"), "value"):
            m_copy["msg_type"] = m_copy["msg_type"].value
        log.append(m_copy)

    return {
        "incident_id": result["incident_id"],
        "report": result["report"],
        "message_log": log,
    }


@app.post("/api/run-live")
def run_live_diagnosis():
    """Run diagnosis using real network telemetry (ping)."""
    try:
        result = run_real_world_diagnosis(target_ip="8.8.8.8")
        
        log = []
        for m in result.get("message_log", []):
            m_copy = dict(m)
            if hasattr(m_copy.get("msg_type"), "value"):
                m_copy["msg_type"] = m_copy["msg_type"].value
            log.append(m_copy)

        return {
            "incident_id": result["incident_id"],
            "report": result["report"],
            "message_log": log,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Live diagnosis failed: {str(e)}")