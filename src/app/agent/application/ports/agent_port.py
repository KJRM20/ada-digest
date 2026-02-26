from typing import Protocol

from src.app.agent.domain.entities.daily_digest import DailyDigest


class AgentPort(Protocol):
    def generate_daily_digest(self) -> DailyDigest: ...
