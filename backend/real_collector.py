"""Collect real network telemetry using ping and run multi-agent diagnosis."""
import subprocess
import platform
import re
import time
from backend.core.orchestrator import Orchestrator


def ping_host(host: str = "8.8.8.8", count: int = 4):
    """
    Perform real ping and extract average latency + packet loss.
    Works on both Windows and Linux/Mac.
    """
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, str(count), host]

    try:
        output = subprocess.check_output(
            command, universal_newlines=True, stderr=subprocess.STDOUT, timeout=15
        )

        if platform.system().lower() == "windows":
            loss_match = re.search(r"\((\d+)% loss\)", output)
            time_match = re.search(r"Average = (\d+)ms", output)

            loss = float(loss_match.group(1)) if loss_match else 0.0
            latency = float(time_match.group(1)) if time_match else 999.0
        else:
            loss_match = re.search(r"(\d+)% packet loss", output)
            time_match = re.search(r"min/avg/max/[^=]*=\s*[\d.]+/([\d.]+)/", output)

            loss = float(loss_match.group(1)) if loss_match else 0.0
            latency = float(time_match.group(1)) if time_match else 999.0

        return latency, loss

    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        # Complete failure
        return 999.0, 100.0


def run_real_world_diagnosis(target_ip: str = "8.8.8.8"):
    print(f"\n📡 [Collector] Pinging {target_ip} to collect real telemetry...")

    latency, loss = ping_host(target_ip, count=4)

    print(f"✅ Real Telemetry → Latency: {latency} ms | Packet Loss: {loss}%")

    # Build scenario in the same format expected by agents
    scenario = {
        "incident_id": f"REAL-{int(time.time())}",
        "telemetry": {
            "latency_ms": latency,
            "jitter_ms": round(latency * 0.12, 2),
            "packet_loss_pct": loss,
            "link_utilization_pct": 45.0,  # Cannot measure without SNMP
        },
        "devices": [
            {
                "device_id": f"TARGET_{target_ip}",
                "status": "up" if loss < 100 else "down",
                "cpu_utilization_pct": 25.0,
                "memory_utilization_pct": 40.0,
                "interface_errors": 0 if loss < 5 else int(loss * 2),
                "queue_drops": 0 if loss < 5 else int(loss * 3),
            }
        ],
        "wifi": {},
    }

    print("🧠 [NetCoop] Feeding real data into Multi-Agent System...\n")

    orch = Orchestrator()
    result = orch.run(scenario)

    report = result.get("report", {})

    print("=" * 60)
    print("🎯 REAL-WORLD DIAGNOSTIC REPORT")
    print("=" * 60)
    print(f"Incident ID : {report.get('incident_id')}")
    print(f"Status      : {str(report.get('status', '')).upper()}")
    print(f"Root Cause  : {report.get('suspected_root_cause')}")
    print(f"Confidence  : {round(report.get('confidence', 0) * 100, 1)}%")
    print(f"Affected    : {report.get('affected_devices')}")
    print("-" * 60)
    print("Recommended Actions:")
    for action in report.get("recommended_actions", []):
        print(f"  • {action}")
    print("=" * 60 + "\n")

    return result


if __name__ == "__main__":
    # You can change the target IP here
    # Examples: "8.8.8.8", "192.168.1.1", "1.1.1.1"
    run_real_world_diagnosis("8.8.8.8")