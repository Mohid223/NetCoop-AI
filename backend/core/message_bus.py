"""In-memory message bus with validation, routing and audit logging."""

from collections import defaultdict
from backend.core.schema import Message


class MessageBus:
    def __init__(self):
        self.log = []
        self._subs = defaultdict(list)
        self.errors = []

    def subscribe(self, name: str, callback):
        if not name or not callable(callback):
            raise ValueError("Valid subscriber name and callback are required")

        if callback not in self._subs[name]:
            self._subs[name].append(callback)

    def publish(self, message: Message):
        if not isinstance(message, Message):
            raise TypeError("Only validated Message objects can be published")

        # Store the serializable message for auditing.
        message_data = message.to_dict()
        self.log.append(message_data)

        # Deliver to all subscribers registered for this recipient.
        subscribers = self._subs.get(message.recipient, [])

        if not subscribers:
            self.errors.append({
                "message_id": message.msg_id,
                "recipient": message.recipient,
                "error": "No subscriber found for recipient"
            })
            return

        for callback in subscribers:
            try:
                callback(message)
            except Exception as exc:
                self.errors.append({
                    "message_id": message.msg_id,
                    "recipient": message.recipient,
                    "error": str(exc)
                })

    def get_log(self):
        return list(self.log)

    def get_errors(self):
        return list(self.errors)