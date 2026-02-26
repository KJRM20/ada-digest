from typing import Protocol

from src.app.agent.domain.entities.daily_digest import DailyDigest
from src.app.notifications.domain.value_objects.email_message import (
    EmailMessage,
)


class RendererPort(Protocol):
    def render(self, digest: DailyDigest) -> EmailMessage: ...
