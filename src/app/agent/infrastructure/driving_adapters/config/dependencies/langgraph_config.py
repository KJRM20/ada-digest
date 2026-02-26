from src.app.agent.infrastructure.driven_adapters.langgraph.adapters.langgraph_agent_adapter import (
    LanggraphAgentAdapter,
)


def get_langgraph_adapter() -> LanggraphAgentAdapter:
    return LanggraphAgentAdapter()
