from pydantic import BaseModel, Field

from src.app.agent.domain.value_objects.news_category import NewsCategory
from src.app.agent.infrastructure.driven_adapters.langgraph.schemas.news_item_schema import (
    NewsItemSchema,
)


class DigestSectionSchema(BaseModel):
    category: NewsCategory = Field(
        description=(
            "Section category. Must be exactly one of the allowed values: "
            "'ai', 'programming', or 'algorithms'. Do NOT translate or "
            "change these values."
        )
    )
    items: list[NewsItemSchema] = Field(
        description="Lista de noticias de la sección"
    )
    curious_fact: str = Field(
        description="Dato curioso relacionado con la categoría"
    )


class DailyDigestSchema(BaseModel):
    sections: list[DigestSectionSchema] = Field(
        description="Secciones del digest diario, una por categoría"
    )
