class RemediationExecutor:

    def execute(self, approval_request):

        if not approval_request:
            raise ValueError("Approval request is required.")

        if approval_request.get("status") != "approved":
            return {
                "success": False,
                "status": "blocked",
                "message": "Human approval is required before execution."
            }

        # No real network changes are performed yet.
        return {
            "success": False,
            "status": "not_configured",
            "message": (
                "No network-device adapter is configured. "
                "The action was not executed."
            )
        }