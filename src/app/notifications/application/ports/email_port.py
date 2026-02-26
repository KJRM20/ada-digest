from typing import Protocol

from src.app.notifications.domain.value_objects.email_message import (
    EmailMessage,
)


class EmailPort(Protocol):
    def send(self, message: EmailMessage) -> None: ...
