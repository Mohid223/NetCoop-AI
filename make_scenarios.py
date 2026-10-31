import json
import os

scenarios = {
    "normal.json": {
        "incident_id": "INC-0001",
        "telemetry": {"latency_ms": 20, "jitter_ms": 2, "packet_loss_pct": 0.1, "link_utilization_pct": 35},
        "devices": [{"device_id": "CORE_SW_01", "status": "up", "cpu_utilization_pct": 30, "interface_errors": 0}],
        "wifi": {}
    },
    "link_congestion.json": {
        "incident_id": "INC-8832",
        "telemetry": {"latency_ms": 280, "jitter_ms": 45, "packet_loss_pct": 3.2, "link_utilization_pct": 94},
        "devices": [{"device_id": "HOSTEL_CORE_SW_01", "status": "up", "cpu_utilization_pct": 88, "queue_drops": 160, "interface_errors": 2}],
        "wifi": {}
    },
    "weak_wifi.json": {
        "incident_id": "INC-4411",
        "telemetry": {"latency_ms": 120, "jitter_ms": 25, "packet_loss_pct": 4.5},
        "devices": [{"device_id": "HOSTEL_AP_03", "status": "up", "cpu_utilization_pct": 40, "interface_errors": 0}],
        "wifi": {"signal_dbm": -82, "retransmission_rate_pct": 22}
    },
    "malformed.json": {
        "incident_id": "INC-9999",
        "telemetry": {"latency_ms": "HIGH", "packet_loss_pct": None},
        "devices": [{"device_id": "BAD_DEV", "status": "down", "cpu_utilization_pct": "N/A"}],
        "wifi": {"signal_dbm": "weak"}
    }
}

out_dir = "backend/data/scenarios"
os.makedirs(out_dir, exist_ok=True)

for name, data in scenarios.items():
    with open(os.path.join(out_dir, name), "w") as f:
        json.dump(data, f, indent=2)
    print(f"Created {name}")

print("\nAll scenarios generated!")