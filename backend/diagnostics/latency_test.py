import re
import subprocess
import platform


class LatencyTest:

    def run(self, host="8.8.8.8", count=5):

        if not re.fullmatch(r"[a-zA-Z0-9.-]+", host):
            raise ValueError("Invalid host.")

        count = max(1, min(int(count), 20))

        windows = platform.system().lower() == "windows"

        command = [
            "ping",
            "-n" if windows else "-c",
            str(count),
            host
        ]

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=30
            )

            output = result.stdout

            times = re.findall(
                r"time[=<]\s*(\d+(?:\.\d+)?)\s*ms",
                output,
                re.IGNORECASE
            )

            values = [float(value) for value in times]

            average = (
                round(sum(values) / len(values), 2)
                if values else None
            )

            return {
                "test": "latency",
                "host": host,
                "success": bool(values),
                "samples_ms": values,
                "average_latency_ms": average,
                "raw_output": output[-1500:]
            }

        except subprocess.TimeoutExpired:
            return {
                "test": "latency",
                "success": False,
                "error": "Latency test timed out."
            }