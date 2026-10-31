# NetCoop AI — Multi-Agent Network Fault Diagnosis System

**An Agentic AI solution for intelligent, explainable network fault diagnosis using collaborative specialized agents.**

NetCoop AI is a multi-agent network diagnosis system designed to identify potential network faults by analyzing telemetry, infrastructure health, and Wi-Fi connectivity data.

Instead of relying on a single diagnostic process, NetCoop AI uses multiple specialized agents that independently analyze network information, exchange structured messages, and collaborate to produce a unified diagnostic report with supporting evidence, confidence scores, and recommended actions.

---

## Problem Statement

Modern campus networks consist of interconnected Wi-Fi access points, routers, switches, Ethernet connections, and other network devices.

When network problems occur, identifying the actual cause can be difficult because network information is distributed across different sources and may be incomplete, inconsistent, or noisy.

NetCoop AI addresses this challenge through a collaborative multi-agent architecture in which specialized agents analyze different aspects of network performance and infrastructure, share their findings, and coordinate to identify likely root causes.

## Key Features

- **Multi-Agent Architecture:** Five specialized agents collaborate to diagnose network issues.
- **Structured Communication:** Agents exchange standardized JSON messages through a custom message protocol.
- **Centralized Orchestration:** An orchestrator coordinates agent execution and manages the diagnostic workflow.
- **Rule-Based Fault Correlation:** Findings from different agents are combined to identify likely root causes.
- **Evidence-Based Diagnosis:** Reports include supporting evidence, affected devices, and alternative causes.
- **Confidence Scoring:** Each diagnosis receives a heuristic confidence score.
- **Actionable Recommendations:** The reporting agent generates suggested troubleshooting steps.
- **REST API:** FastAPI endpoints support scenario-based and live ping-based diagnosis.
- **JSON Reports:** Diagnostic results and agent communication logs can be saved for inspection.

## System Architecture

NetCoop AI follows a collaborative multi-agent architecture.

```text
                  User / Network Scenario
                            |
                            v
                    FastAPI Application
                            |
                            v
                       Orchestrator
                            |
             +--------------+--------------+
             |              |              |
             v              v              v
       Performance     Infrastructure   Connectivity
          Agent            Agent           Agent
             |              |              |
             +--------------+--------------+
                            |
                            v
                   Message Bus
                            |
                            v
                Fault Correlation Agent
                            |
                            v
                    Reporting Agent
                            |
                            v
                  Unified Diagnostic
                        Report
                            |
                            v
                    JSON Output
```

### Specialized Agents

| Agent | Responsibility |
|---|---|
| Performance Agent | Analyzes latency, jitter, packet loss, and link utilization. |
| Infrastructure Agent | Checks device availability, CPU utilization, memory utilization, queue drops, and interface errors. |
| Connectivity Agent | Analyzes Wi-Fi signal strength and retransmission rate. |
| Fault Correlation Agent | Combines findings and identifies likely root causes using rule-based scoring. |
| Reporting Agent | Generates diagnostic reports and recommends troubleshooting actions. |

## Agent Communication Protocol

NetCoop AI uses a custom structured JSON message protocol to enable communication between specialized agents.

Each message contains:

| Field | Description |
|---|---|
| sender | Name of the sending agent |
| recipient | Intended receiving agent |
| msg_type | Message type |
| incident_id | Unique incident identifier |
| payload | Diagnostic data or findings |
| confidence | Agent confidence score, when provided |
| units | Optional metric unit information |
| msg_id | Unique message identifier |
| timestamp | UTC message timestamp |

### Supported Message Types

- `REQUEST` — Requests an agent to perform analysis.
- `FINDING` — Shares diagnostic findings.
- `ERROR` — Reports an input or processing problem.
- `RESULT` — Delivers the correlated diagnostic result.

The message schema is defined in `backend/core/schema.py`, while `backend/core/message_bus.py` implements synchronous in-memory message delivery.

## Diagnostic Workflow

1. A user submits a network scenario through the API or CLI.
2. The Orchestrator generates or accepts an incident ID.
3. The specialized agents receive their respective diagnostic requests.
4. Each agent analyzes its assigned network metrics and generates findings.
5. Findings are sent to the Fault Correlation Agent.
6. The Fault Correlation Agent evaluates anomalies using predefined rules and confidence weights.
7. The Reporting Agent receives the correlated result.
8. A unified diagnostic report is generated and saved as a JSON file.

## Root Cause Detection

The Fault Correlation Agent evaluates anomalies such as:

| Detected Anomaly | Possible Root Cause |
|---|---|
| High link utilization | Link congestion |
| Queue drops | Egress queue congestion |
| Packet loss | Link instability |
| High latency | Possible network congestion |
| High jitter | Network instability |
| Weak Wi-Fi signal | Poor wireless connectivity |
| High retransmission rate | Wi-Fi retransmission storm |
| Interface errors | Ethernet/interface fault |
| Device down | Hardware failure or unreachable device |
| High CPU utilization | Device CPU overload |
| High memory utilization | Memory pressure |

The agent ranks possible causes using predefined weights and produces a confidence score based on the relative scores of competing causes.

**Important:** The confidence score is a heuristic ranking score, not a statistically calibrated probability. If the available evidence is insufficient, the system can return an `insufficient_evidence` status rather than asserting a definite root cause.

## Diagnostic Report

The Reporting Agent generates a unified report containing:

- `incident_id`
- `status`
- `suspected_root_cause`
- `confidence`
- `affected_devices`
- `supporting_evidence`
- `alternative_causes`
- `recommended_actions`
- `evidence_sources`
- `limitations`

Reports are saved in:

```text
backend/outputs/
```

Agent communication logs can also be saved for reviewing the diagnostic workflow.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend implementation |
| FastAPI | REST API development |
| Pydantic | API request validation |
| JSON | Scenario input and diagnostic output |
| Custom Message Bus | Inter-agent communication |
| Rule-Based Engine | Fault correlation and diagnosis |
| Uvicorn | ASGI server |

## Project Structure

```text
NetCoop-AI/
│
├── backend/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py
│   │   ├── connectivity_agent.py
│   │   ├── fault_correlation_agent.py
│   │   ├── infrastructure_agent.py
│   │   ├── reporting_agent.py
│   │   └── telemetry_agent.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── message_bus.py
│   │   ├── orchestrator.py
│   │   └── schema.py
│   │
│   ├── data/
│   │   └── scenarios/
│   │
│   ├── outputs/
│   │
│   ├── __init__.py
│   ├── api.py
│   ├── main.py
│   └── real_collector.py
│
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/NetCoop-AI.git
cd NetCoop-AI
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install fastapi uvicorn pydantic
```

### 4. Start the Backend Server

Run the following command from the project root directory:

```bash
uvicorn backend.api:app --reload
```

The backend API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Checks backend service status. |
| GET | `/api/scenarios` | Lists available JSON diagnostic scenarios. |
| POST | `/api/run` | Runs diagnosis using a scenario JSON file. |
| POST | `/api/run-live` | Runs ping-based diagnosis against a target IP. |

### Example: Health Check

```http
GET /api/health
```

Example response:

```json
{
  "status": "ok",
  "service": "NetCoop AI"
}
```

### Example: Run Scenario Diagnosis

```http
POST /api/run
Content-Type: application/json
```

Request:

```json
{
  "scenario_file": "congestion.json"
}
```

The scenario file must exist in the backend scenario directory.

### Example: Run Live Diagnosis

```http
POST /api/run-live
Content-Type: application/json
```

Request:

```json
{}
```

The current implementation uses `8.8.8.8` as the default ping target.

## Scenario Input Format

Scenario-based diagnosis accepts JSON input containing telemetry, device information, and Wi-Fi metrics.

Example:

```json
{
  "incident_id": "INC-001",
  "telemetry": {
    "latency_ms": 120,
    "jitter_ms": 20,
    "packet_loss_pct": 3,
    "link_utilization_pct": 92
  },
  "devices": [
    {
      "device_id": "SWITCH-01",
      "status": "up",
      "cpu_utilization_pct": 45,
      "memory_utilization_pct": 60,
      "interface_errors": 2,
      "queue_drops": 10
    }
  ],
  "wifi": {
    "signal_dbm": -82,
    "retransmission_rate_pct": 18
  }
}
```

This is an illustrative input format for the implemented agents. Thresholds are defined in their respective agent files.

## Live Network Diagnosis

NetCoop AI includes a basic real-world diagnostic collector in:

```text
backend/real_collector.py
```

The collector uses the system ping command to measure:

- Average network latency
- Packet loss

It then creates a diagnostic scenario and passes it through the multi-agent system.

**Current implementation limitation:** Jitter is estimated from measured latency. Link utilization is assigned a placeholder value, while CPU, memory, and other device metrics are generated as scenario values. These metrics are not directly collected from routers, switches, or access points through SNMP or another network-management interface.

Therefore, live diagnosis currently provides ping-based connectivity information rather than complete campus network telemetry collection.

## Current Implementation Notes

- The message bus uses synchronous in-memory communication; it does not provide persistent message storage.
- The agents use predefined thresholds and rule-based correlation rather than a trained machine-learning fault classifier.
- The current correlation workflow expects findings from three diagnostic agents. If an agent returns only an error instead of a finding, the correlation workflow may not complete.
- The protocol includes a `units` field, but the current agents do not consistently populate it.
- The diagnostic confidence score is heuristic and should not be interpreted as a probability.
- Live collection does not currently provide direct SNMP-based infrastructure monitoring.

## Future Enhancements

- Integration with SNMP for real-time router and switch monitoring.
- Support for additional network telemetry sources.
- Improved handling of missing, malformed, and inconsistent agent responses.
- More robust orchestration and agent failure recovery.
- Persistent message storage and incident history.
- Expanded interoperability validation and automated scenario testing.
- More advanced fault correlation and evidence reconciliation.
- Integration with network monitoring platforms.

## Hackathon Objective

NetCoop AI aims to demonstrate how specialized AI agents can collaborate to diagnose complex network problems through structured communication, coordinated analysis, and explainable results.

The system focuses on identifying likely root causes, presenting supporting evidence, highlighting uncertainty, and providing practical troubleshooting recommendations.

---

**NetCoop AI — Collaborative Intelligence for Smarter Network Diagnosis.**