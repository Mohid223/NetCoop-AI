class RootCauseEngine:

    def analyze(self, telemetry: dict):

        candidates = []

        latency = telemetry.get("latency")
        packet_loss = telemetry.get("packet_loss")
        jitter = telemetry.get("jitter")
        cpu = telemetry.get("cpu_usage")
        memory = telemetry.get("memory_usage")

        if packet_loss is not None and packet_loss >= 5:
            candidates.append({
                "cause": "Possible connectivity degradation",
                "evidence": [
                    f"Packet loss is {packet_loss}%"
                ],
                "priority": "high"
            })

        if latency is not None and latency >= 150:
            candidates.append({
                "cause": "Possible network congestion or routing delay",
                "evidence": [
                    f"Latency is {latency} ms"
                ],
                "priority": "high"
            })

        if jitter is not None and jitter >= 30:
            candidates.append({
                "cause": "Possible unstable network performance",
                "evidence": [
                    f"Jitter is {jitter} ms"
                ],
                "priority": "medium"
            })

        if cpu is not None and cpu >= 90:
            candidates.append({
                "cause": "Possible infrastructure CPU overload",
                "evidence": [
                    f"CPU usage is {cpu}%"
                ],
                "priority": "high"
            })

        if memory is not None and memory >= 90:
            candidates.append({
                "cause": "Possible infrastructure memory pressure",
                "evidence": [
                    f"Memory usage is {memory}%"
                ],
                "priority": "high"
            })

        if not candidates:
            return {
                "status": "inconclusive",
                "primary_cause": None,
                "candidates": [],
                "message": "Insufficient abnormal evidence to identify a root cause."
            }

        priority_order = {
            "high": 3,
            "medium": 2,
            "low": 1
        }

        candidates.sort(
            key=lambda item: priority_order[item["priority"]],
            reverse=True
        )

        return {
            "status": "candidate_found",
            "primary_cause": candidates[0],
            "candidates": candidates,
            "message": (
                "Potential root causes identified. "
                "Further diagnostic tests are required for confirmation."
            )
        }