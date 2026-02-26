from src.app.agent.domain.entities.daily_digest import DailyDigest
from src.app.agent.domain.value_objects.digest_section import DigestSection
from src.app.agent.domain.value_objects.news_category import NewsCategory
from src.app.agent.domain.value_objects.news_item import NewsItem
from src.app.agent.infrastructure.driven_adapters.langgraph.handlers.agent_handler import (
    AgentHandler,
)
from src.app.agent.infrastructure.driven_adapters.langgraph.schemas.daily_digest_schema import (
    DailyDigestSchema,
)


class LanggraphAgentAdapter:
    def __init__(self) -> None:
        self._handler = AgentHandler()

    def generate_daily_digest(self) -> DailyDigest:
        schema: DailyDigestSchema = self._handler.run()
        return self._map_to_domain(schema)

    def _map_to_domain(self, schema: DailyDigestSchema) -> DailyDigest:
        sections = []
        for section_schema in schema.sections:
            try:
                category = NewsCategory(section_schema.category)
            except ValueError:
                category = NewsCategory.PROGRAMMING

            items = [
                NewsItem(
                    title=item.title,
                    summary=item.summary,
                    url=item.url,
                    category=category,
                )
                for item in section_schema.items
            ]

            sections.append(
                DigestSection(
                    category=category,
                    items=items,
                    curious_fact=section_schema.curious_fact,
                )
            )

        return DailyDigest(sections=sections)
