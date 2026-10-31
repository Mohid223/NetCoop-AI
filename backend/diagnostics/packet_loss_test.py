import re
import subprocess
import platform


class PacketLossTest:

    def run(self, host="8.8.8.8", count=10):

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

            if windows:
                match = re.search(
                    r"(\d+)%\s*loss",
                    output,
                    re.IGNORECASE
                )
            else:
                match = re.search(
                    r"(\d+(?:\.\d+)?)%\s*packet loss",
                    output,
                    re.IGNORECASE
                )

            loss = float(match.group(1)) if match else None

            return {
                "test": "packet_loss",
                "host": host,
                "success": result.returncode == 0,
                "packet_loss_percent": loss,
                "raw_output": output[-2000:]
            }

        except subprocess.TimeoutExpired:
            return {
                "test": "packet_loss",
                "host": host,
                "success": False,
                "error": "Packet loss test timed out."
            }