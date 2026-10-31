from collections import Counter


class PatternDetector:

    def analyze(self, incidents):

        causes = []

        for record in incidents:
            incident = record.get("incident", {})
            analysis = incident.get("root_cause_analysis", {})

            primary = analysis.get("primary_cause")

            if primary and primary.get("cause"):
                causes.append(primary["cause"])

        counts = Counter(causes)

        patterns = [
            {
                "pattern": cause,
                "occurrences": count
            }
            for cause, count in counts.items()
            if count >= 2
        ]

        return {
            "total_incidents_analyzed": len(incidents),
            "repeated_patterns": patterns
        }