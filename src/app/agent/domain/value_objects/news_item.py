from dataclasses import dataclass

from src.app.agent.domain.value_objects.news_category import NewsCategory


@dataclass(frozen=True)
class NewsItem:
    title: str
    summary: str
    url: str
    category: NewsCategory
