from datetime import datetime, timezone


class RollbackManager:

    def __init__(self):
        self.rollback_records = []

    def create_record(self, action, previous_state):

        record = {
            "action": action,
            "previous_state": previous_state,
            "status": "rollback_information_saved",
            "created_at": datetime.now(timezone.utc).isoformat()
        }

        self.rollback_records.append(record)

        return record

    def list_records(self):
        return self.rollback_records