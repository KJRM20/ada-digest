from src.app.agent.application.ports.agent_port import AgentPort
from src.app.agent.domain.entities.daily_digest import DailyDigest


class GenerateDailyDigestUseCase:
    def __init__(self, agent_port: AgentPort) -> None:
        self._agent_port = agent_port

    def execute(self) -> DailyDigest:
        return self._agent_port.generate_daily_digest()
