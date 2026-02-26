import httpx
from langchain_groq import ChatGroq

from src.app.agent.infrastructure.driven_adapters.langgraph.prompts.summary_prompt import (
    summary_prompt,
)
from src.app.agent.infrastructure.driven_adapters.langgraph.schemas.daily_digest_schema import (
    DailyDigestSchema,
)

_HN_SEARCH_URL = "https://hn.algolia.com/api/v1/search"
_DEVTO_API_URL = "https://dev.to/api/articles"

_CATEGORIES = ["ai", "programming", "algorithms"]

_CATEGORY_QUERIES: dict[str, str] = {
    "ai": "artificial intelligence OR LLM OR machine learning",
    "programming": "programming languages OR frameworks OR tools",
    "algorithms": "algorithms OR data structures OR code optimization",
}

_DEVTO_TAGS: dict[str, str] = {
    "ai": "ai",
    "programming": "webdev",
    "algorithms": "algorithms",
}

_CURIOUS_TOPICS: dict[str, str] = {
    "ai": "modelos de lenguaje y aprendizaje automático",
    "programming": "lenguajes de programación y patrones de diseño",
    "algorithms": "algoritmos y estructuras de datos",
}


class AgentHandler:
    def __init__(self) -> None:
        # Each model has an independent daily token quota on Groq free tier.
        self._llm_extractor = ChatGroq(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0,
        )
        self._llm_summarize = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.7,
        )
        self._llm_fact = ChatGroq(
            model="meta-llama/llama-4-maverick-17b-128e-instruct",
            temperature=0.7,
        )

    def _fetch_news(self, category: str) -> str:
        """Fetch raw news titles and URLs via HTTP — no LLM involved."""
        query = _CATEGORY_QUERIES[category]
        tag = _DEVTO_TAGS[category]
        results: list[str] = []

        try:
            resp = httpx.get(
                _HN_SEARCH_URL,
                params={"query": query, "hitsPerPage": 5},
                timeout=10,
            )
            resp.raise_for_status()
            for hit in resp.json().get("hits", [])[:5]:
                title = hit.get("title", "")
                url = hit.get("url") or ""
                if title:
                    results.append(f"- {title} | {url}")
        except Exception:
            pass

        try:
            resp = httpx.get(
                _DEVTO_API_URL,
                params={"tag": tag, "per_page": 3},
                timeout=10,
            )
            resp.raise_for_status()
            for article in resp.json()[:3]:
                title = article.get("title", "")
                url = article.get("url", "")
                if title:
                    results.append(f"- {title} | {url}")
        except Exception:
            pass

        if not results:
            return f"No se encontraron noticias para '{category}'."
        return f"Noticias de '{category}':\n" + "\n".join(results)

    def _summarize(self, raw: str) -> str:
        chain = summary_prompt | self._llm_summarize
        return str(chain.invoke({"raw_articles": raw}).content)

    def _fetch_curious_fact(self, category: str) -> str:
        topic = _CURIOUS_TOPICS[category]
        response = self._llm_fact.invoke(
            f"Dame un dato curioso, educativo y breve (máximo 3 oraciones) "
            f"sobre {topic} dirigido a programadores. "
            f"Debe ser técnicamente preciso e interesante."
        )
        return str(response.content)

    def run(self) -> DailyDigestSchema:
        # Step 1: fetch news directly via HTTP — no agent loop, no LLM.
        raw_by_cat = {cat: self._fetch_news(cat) for cat in _CATEGORIES}

        # Step 2: summarize and get curious facts per category.
        sections_parts: list[str] = []
        for cat in _CATEGORIES:
            summarized = self._summarize(raw_by_cat[cat])
            fact = self._fetch_curious_fact(cat)
            sections_parts.append(
                f"## Categoría: {cat}\n{summarized}\nDato curioso: {fact}"
            )

        compiled = "\n\n".join(sections_parts)

        # Step 3: extract structured digest from the compiled content.
        extractor = self._llm_extractor.with_structured_output(
            DailyDigestSchema
        )
        return extractor.invoke(
            "Extrae y devuelve el digest estructurado a partir de este "
            "contenido. Agrupa los artículos por categoría usando exactamente "
            "los valores 'ai', 'programming' o 'algorithms' en el campo "
            "category. Usa los títulos y URLs EXACTOS del texto sin "
            "modificarlos. Asigna el dato curioso correspondiente a cada "
            f"sección.\n\n{compiled}"
        )
