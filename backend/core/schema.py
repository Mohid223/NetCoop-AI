 
"""NetCoop Protocol v1.0 — Validated inter-agent communication schema."""

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
import uuid


PROTOCOL_VERSION = "1.0"


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

    schema_version: str = PROTOCOL_VERSION

    def __post_init__(self):
        # Validate required identifiers
        if not isinstance(self.sender, str) or not self.sender.strip():
            raise ValueError("Message sender cannot be empty")

        if not isinstance(self.recipient, str) or not self.recipient.strip():
            raise ValueError("Message recipient cannot be empty")

        if not isinstance(self.incident_id, str) or not self.incident_id.strip():
            raise ValueError("Incident ID cannot be empty")

        # Validate message type
        if isinstance(self.msg_type, str):
            try:
                self.msg_type = MsgType(self.msg_type.upper())
            except ValueError:
                raise ValueError(
                    f"Unsupported message type: {self.msg_type}"
                )

        if not isinstance(self.msg_type, MsgType):
            raise ValueError("Invalid message type")

        # Validate payload
        if not isinstance(self.payload, dict):
            raise ValueError("Message payload must be a dictionary")

        # Validate confidence
        if self.confidence is not None:
            if isinstance(self.confidence, bool) or not isinstance(
                self.confidence, (int, float)
            ):
                raise ValueError("Confidence must be a number")

            if not 0.0 <= self.confidence <= 1.0:
                raise ValueError("Confidence must be between 0 and 1")

        # Validate units
        if not isinstance(self.units, dict):
            raise ValueError("Units must be a dictionary")

        # Validate protocol version
        if self.schema_version != PROTOCOL_VERSION:
            raise ValueError(
                f"Unsupported schema version: {self.schema_version}"
            )

    def to_dict(self):
        """Return a JSON-serializable message dictionary."""
        data = asdict(self)
        data["msg_type"] = self.msg_type.value
        return data
