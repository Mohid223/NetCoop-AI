from datetime import datetime, timezone
from uuid import uuid4


class IncidentMemory:

    def __init__(self):
        self.incidents = []

    def save(self, incident):

        record = {
            "incident_id": str(uuid4()),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "incident": incident
        }

        self.incidents.append(record)

        return record

    def get_all(self):
        return self.incidents

    def get_by_id(self, incident_id):

        for record in self.incidents:
            if record["incident_id"] == incident_id:
                return record

        return None

    def clear(self):
        self.incidents.clear()