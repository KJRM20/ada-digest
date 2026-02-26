from dataclasses import dataclass, field

from src.app.agent.domain.value_objects.news_category import NewsCategory
from src.app.agent.domain.value_objects.news_item import NewsItem


@dataclass(frozen=True)
class DigestSection:
    category: NewsCategory
    items: list[NewsItem] = field(default_factory=list)
    curious_fact: str = ""
