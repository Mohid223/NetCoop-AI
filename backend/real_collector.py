
"""Collect real network telemetry using ping and run multi-agent diagnosis."""

import subprocess
import platform
import re

from backend.core.orchestrator import Orchestrator


def ping_host(host: str = "8.8.8.8", count: int = 4):
    """
    Perform real ping and extract average latency and packet loss.
    Supports Windows, Linux and macOS.
    """

    is_windows = platform.system().lower() == "windows"

    count_flag = "-n" if is_windows else "-c"

    command = [
        "ping",
        count_flag,
        str(count),
        host
    ]

    try:
        output = subprocess.check_output(
            command,
            universal_newlines=True,
            stderr=subprocess.STDOUT,
            timeout=20
        )

    except subprocess.CalledProcessError as error:
        output = error.output or ""

    except subprocess.TimeoutExpired:
        print("Ping timed out.")
        return 999.0, 100.0

    except FileNotFoundError:
        print("Ping command not found.")
        return 999.0, 100.0

    # Extract packet loss
    if is_windows:
        loss_match = re.search(
            r"\((\d+(?:\.\d+)?)%\s*loss\)",
            output,
            re.IGNORECASE
        )

        latency_match = re.search(
            r"Average\s*=\s*(\d+)\s*ms",
            output,
            re.IGNORECASE
        )

    else:
        loss_match = re.search(
            r"(\d+(?:\.\d+)?)%\s*packet loss",
            output,
            re.IGNORECASE
        )

        latency_match = re.search(
            r"=\s*[\d.]+/([\d.]+)/[\d.]+",
            output
        )

    # Avoid treating an unparsed response as a successful ping
    loss = float(loss_match.group(1)) if loss_match else 100.0
    latency = float(latency_match.group(1)) if latency_match else 999.0

    return latency, loss


def run_real_world_diagnosis(target_ip: str = "8.8.8.8"):

    print(f"\n[Collector] Pinging {target_ip}...")

    latency, loss = ping_host(target_ip, count=4)

    print(
        f"Real Telemetry -> Latency: {latency} ms | "
        f"Packet Loss: {loss}%"
    )

    # Build scenario for the multi-agent system
    scenario = {
        "incident_id": "LIVE-NETWORK-DIAGNOSIS",

        "telemetry": {
            "latency_ms": latency,
            "jitter_ms": round(latency * 0.12, 2),
            "packet_loss_pct": loss,

            # These are estimates/placeholders, not measured values.
            "link_utilization_pct": 45.0,
        },

        "devices": [
            {
                "device_id": "LIVE-DEVICE-01",
                "cpu_usage": 25.0,
                "memory_usage": 40.0,
                "interface_errors": int(loss),
                "queue_drops": int(loss),
            }
        ],

        # Enable autonomous diagnostic tests
        "run_diagnostics": True,
        "target_host": target_ip,
    }

    print("\n[NetCoop] Starting Multi-Agent Diagnosis...\n")

    orchestrator = Orchestrator()

    result = orchestrator.run(scenario)

    report = result.get("report", {})

    print("=" * 60)
    print("REAL-WORLD DIAGNOSTIC REPORT")
    print("=" * 60)

    print(f"Incident ID : {report.get('incident_id')}")
    print(f"Status      : {str(report.get('status', '')).upper()}")
    print(f"Root Cause  : {report.get('suspected_root_cause')}")

    confidence = report.get("confidence", 0)

    print(f"Confidence  : {round(confidence * 100, 1)}%")
    print(f"Affected    : {report.get('affected_devices')}")

    print("-" * 60)
    print("Recommended Actions:")

    for action in report.get("recommended_actions", []):
        print(f"  - {action}")

    print("=" * 60)

    # Autonomous investigation results
    investigation = result.get("autonomous_investigation", {})

    print("\nAUTONOMOUS INVESTIGATION")
    print("=" * 60)

    print(
        "Investigation Status:",
        investigation.get("investigation_status")
    )

    print(
        "Investigation Mode:",
        investigation.get("mode")
    )

    print(
        "Diagnostic Tests:",
        len(investigation.get("diagnostic_results", []))
    )

    for diagnostic in investigation.get("diagnostic_results", []):
        print(
            f"- {diagnostic.get('test')}: "
            f"{diagnostic.get('status', diagnostic.get('success', 'Unknown'))}"
        )

    print("=" * 60)

    return result


if __name__ == "__main__":
    run_real_world_diagnosis("8.8.8.8")
