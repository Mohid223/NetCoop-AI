class DecisionEngine:

    def select_checks(self, telemetry: dict):

        checks = []

        latency = telemetry.get("latency")
        packet_loss = telemetry.get("packet_loss")
        cpu = telemetry.get("cpu_usage")
        dns_status = telemetry.get("dns_status")

        if packet_loss is None or packet_loss > 1:
            checks.append("packet_loss_test")

        if latency is None or latency > 80:
            checks.append("latency_test")

        if dns_status is None:
            checks.append("dns_test")

        if cpu is None or cpu > 80:
            checks.append("interface_test")

        if not checks:
            checks.append("ping_test")

        return checks

    def create_plan(self, root_cause: dict, telemetry: dict):

        checks = self.select_checks(telemetry)

        primary_cause = root_cause.get("primary_cause")

        return {
            "plan_status": "pending",
            "execution_mode": "diagnostic_only",

            "suspected_cause": (
                primary_cause.get("cause")
                if primary_cause else None
            ),

            "planned_checks": [
                {
                    "test": check,
                    "status": "pending"
                }
                for check in checks
            ],

            "configuration_changes_allowed": False
        }