"""In-memory pub/sub bus with full audit log."""
from collections import defaultdict


class MessageBus:
    def __init__(self):
        self.log = []
        self._subs = defaultdict(list)

    def subscribe(self, name: str, callback):
        self._subs[name].append(callback)

    def publish(self, message):
        # Store serializable version in log
        self.log.append(message.to_dict())

        # Deliver to subscribers
        for callback in self._subs.get(message.recipient, []):
            callback(message)

    def get_log(self):
        return list(self.log)