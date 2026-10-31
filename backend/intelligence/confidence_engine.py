class ConfidenceEngine:

    REQUIRED_METRICS = [
        "latency",
        "packet_loss",
        "jitter",
        "cpu_usage",
        "memory_usage",
    ]

    def calculate(self, telemetry: dict, evidence_count: int = 0):

        available = [
            metric
            for metric in self.REQUIRED_METRICS
            if telemetry.get(metric) is not None
        ]

        missing = [
            metric
            for metric in self.REQUIRED_METRICS
            if telemetry.get(metric) is None
        ]

        completeness = (
            len(available) / len(self.REQUIRED_METRICS)
        ) * 100

        evidence_score = min(evidence_count * 10, 30)

        score = min(
            round(completeness * 0.7 + evidence_score, 2),
            100
        )

        return {
            "score": score,
            "available_metrics": available,
            "missing_metrics": missing,
            "completeness": round(completeness, 2),

            "interpretation": (
                "High evidence coverage" if score >= 80
                else "Moderate evidence coverage" if score >= 50
                else "Low evidence coverage"
            ),

            "note": (
                "This is an evidence-coverage score, "
                "not a calibrated probability of correctness."
            )
        }