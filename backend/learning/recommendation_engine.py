class RecommendationEngine:

    def generate(self, root_cause, patterns=None):

        recommendations = []

        primary = root_cause.get("primary_cause")

        if primary:
            cause = primary.get("cause", "")

            if "connectivity" in cause.lower():
                recommendations.append(
                    "Inspect network links, interface errors and upstream connectivity."
                )

            elif "congestion" in cause.lower():
                recommendations.append(
                    "Review traffic utilization, routing and QoS policies."
                )

            elif "cpu" in cause.lower():
                recommendations.append(
                    "Identify CPU-intensive processes and review device workload."
                )

            elif "memory" in cause.lower():
                recommendations.append(
                    "Inspect memory-intensive processes and memory trends."
                )

        for pattern in (patterns or {}).get("repeated_patterns", []):
            recommendations.append(
                f"Repeated incident detected: {pattern['pattern']} "
                f"({pattern['occurrences']} occurrences). "
                "Investigate the underlying recurring issue."
            )

        if not recommendations:
            recommendations.append(
                "Collect more telemetry before suggesting a specific repair."
            )

        return list(dict.fromkeys(recommendations))