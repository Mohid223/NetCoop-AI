import platform
import subprocess
import re


class PingTest:

    def run(self, host="8.8.8.8", timeout=5):

        if not re.fullmatch(r"[a-zA-Z0-9.-]+", host):
            raise ValueError("Invalid host.")

        count_flag = "-n" if platform.system().lower() == "windows" else "-c"
        timeout_flag = "-w" if platform.system().lower() == "windows" else "-W"

        command = [
            "ping",
            count_flag, "4",
            timeout_flag, str(timeout),
            host
        ]

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout + 5
            )

            return {
                "test": "ping",
                "host": host,
                "success": result.returncode == 0,
                "output": result.stdout[-2000:],
                "error": result.stderr[-1000:]
            }

        except subprocess.TimeoutExpired:
            return {
                "test": "ping",
                "host": host,
                "success": False,
                "error": "Ping command timed out."
            }

        except FileNotFoundError:
            return {
                "test": "ping",
                "host": host,
                "success": False,
                "error": "Ping command is unavailable."
            }