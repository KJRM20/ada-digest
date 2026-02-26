from pydantic import BaseModel, Field

from src.app.agent.domain.value_objects.news_category import NewsCategory


class NewsItemSchema(BaseModel):
    title: str = Field(description="Título del artículo o noticia")
    summary: str = Field(description="Resumen técnico breve del contenido")
    url: str = Field(description="URL fuente del artículo")
    category: NewsCategory = Field(
        description=(
            "Article category. Must be exactly one of the allowed values: "
            "'ai', 'programming', or 'algorithms'. Do NOT translate or "
            "change these values."
        )
    )
