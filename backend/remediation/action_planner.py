class ActionPlanner:

    ACTIONS = {
        "Possible connectivity degradation": {
            "action": "inspect_network_link",
            "risk": "medium",
            "description": "Inspect network link and interface errors."
        },
        "Possible network congestion or routing delay": {
            "action": "inspect_routing_and_traffic",
            "risk": "medium",
            "description": "Review routing path and traffic utilization."
        },
        "Possible infrastructure CPU overload": {
            "action": "inspect_cpu_processes",
            "risk": "low",
            "description": "Identify processes consuming excessive CPU."
        },
        "Possible infrastructure memory pressure": {
            "action": "inspect_memory_usage",
            "risk": "low",
            "description": "Inspect memory utilization and processes."
        }
    }

    def create_plan(self, root_cause):

        cause = root_cause.get("primary_cause")

        if not cause:
            return {
                "status": "no_action",
                "reason": "No sufficiently supported cause identified.",
                "actions": []
            }

        cause_name = cause.get("cause")

        action = self.ACTIONS.get(cause_name)

        if not action:
            return {
                "status": "manual_review",
                "actions": [],
                "reason": "No predefined remediation plan matches this cause."
            }

        return {
            "status": "approval_required",
            "actions": [action],
            "requires_human_approval": True,
            "execution_enabled": False
        }