from datetime import datetime, timezone
from uuid import uuid4


class ApprovalManager:

    def __init__(self):
        self.requests = {}

    def request_approval(self, action):

        approval_id = str(uuid4())

        request = {
            "approval_id": approval_id,
            "action": action,
            "status": "pending",
            "created_at": datetime.now(timezone.utc).isoformat()
        }

        self.requests[approval_id] = request

        return request

    def approve(self, approval_id):

        request = self.requests.get(approval_id)

        if not request:
            raise ValueError("Approval request not found.")

        if request["status"] != "pending":
            raise ValueError("Approval request is no longer pending.")

        request["status"] = "approved"

        return request

    def reject(self, approval_id):

        request = self.requests.get(approval_id)

        if not request:
            raise ValueError("Approval request not found.")

        if request["status"] != "pending":
            raise ValueError("Approval request is no longer pending.")

        request["status"] = "rejected"

        return request

    def get_request(self, approval_id):
        return self.requests.get(approval_id)