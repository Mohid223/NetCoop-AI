"""NetCoop Protocol v1.0 — Message schema for inter-agent communication."""
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
import uuid


class MsgType(str, Enum):
    REQUEST = "REQUEST"
    FINDING = "FINDING"
    ERROR = "ERROR"
    RESULT = "RESULT"


@dataclass
class Message:
    sender: str
    recipient: str
    msg_type: MsgType
    incident_id: str
    payload: dict
    confidence: float = None
    units: dict = field(default_factory=dict)
    msg_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self):
        data = asdict(self)
        # Make enum JSON serializable
        if isinstance(data.get("msg_type"), MsgType):
            data["msg_type"] = data["msg_type"].value
        return data