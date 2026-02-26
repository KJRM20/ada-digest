from src.app.agent.application.use_cases.generate_daily_digest import (
    GenerateDailyDigestUseCase,
)
from src.app.agent.infrastructure.driving_adapters.config.dependencies.langgraph_config import (
    get_langgraph_adapter,
)


def get_generate_daily_digest_use_case() -> GenerateDailyDigestUseCase:
    return GenerateDailyDigestUseCase(agent_port=get_langgraph_adapter())
