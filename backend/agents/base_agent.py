"""Base agent class — all agents inherit from this."""
from backend.core.schema import Message, MsgType


class BaseAgent:
    name = "base"

    def __init__(self, bus):
        self.bus = bus
        self.bus.subscribe(self.name, self.receive)

    def receive(self, message):
        if message.recipient == self.name:
            self.handle(message)

    def handle(self, message):
        raise NotImplementedError

    def send(self, recipient, msg_type, incident_id, payload, confidence=None):
        msg = Message(
            sender=self.name,
            recipient=recipient,
            msg_type=msg_type,
            incident_id=incident_id,
            payload=payload,
            confidence=confidence,
        )
        self.bus.publish(msg)
        return msg