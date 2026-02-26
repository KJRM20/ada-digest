from collections.abc import Collection, Sequence
import os
from pathlib import Path

import jinja2

from src.app.agent.domain.entities.daily_digest import DailyDigest
from src.app.agent.domain.value_objects.news_category import NewsCategory
from src.app.notifications.domain.value_objects.email_message import (
    EmailMessage,
)

_TEMPLATES_DIR = Path(__file__).parent.parent / "templates"

_CATEGORY_LABELS: dict[NewsCategory, str] = {
    NewsCategory.AI: "Inteligencia Artificial",
    NewsCategory.PROGRAMMING: "Programación",
    NewsCategory.ALGORITHMS: "Algoritmos",
}

_EMAIL_SUBJECT = "Ada · Digest Diario para Programadores"


class JinjaRendererAdapter:
    def __init__(self) -> None:
        self._env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(_TEMPLATES_DIR)),
            autoescape=jinja2.select_autoescape(["html"]),
        )
        self._recipient = os.environ["GMAIL_RECIPIENT"]

    def render(self, digest: DailyDigest) -> EmailMessage:
        template = self._env.get_template("digest.html.j2")
        sections_ctx = self._build_sections_context(digest)
        generated_at = digest.generated_at.strftime("%d %b %Y")

        html_body = template.render(
            sections=sections_ctx,
            generated_at=generated_at,
        )
        plain_body = self._build_plain_body(digest, generated_at)

        return EmailMessage(
            subject=_EMAIL_SUBJECT,
            html_body=html_body,
            plain_body=plain_body,
            recipient=self._recipient,
        )

    def _build_sections_context(
        self, digest: DailyDigest
    ) -> list[dict[str, Sequence[Collection[str]]]]:
        sections = []
        for section in digest.sections:
            label = _CATEGORY_LABELS.get(section.category, section.category)
            items = [
                {
                    "title": item.title,
                    "summary": item.summary,
                    "url": item.url,
                }
                for item in section.items
            ]
            sections.append(
                {
                    "category_label": label,
                    "news_items": items,
                    "curious_fact": section.curious_fact,
                }
            )
        return sections

    def _build_plain_body(self, digest: DailyDigest, generated_at: str) -> str:
        lines: list[str] = [
            "Ada · Digest Diario para Programadores",
            f"Generado el {generated_at}",
            "",
        ]
        for section in digest.sections:
            label = _CATEGORY_LABELS.get(section.category, section.category)
            lines.append(f"== {label} ==")
            for item in section.items:
                lines.append(f"- {item.title}")
                lines.append(f"  {item.summary}")
                lines.append(f"  {item.url}")
            if section.curious_fact:
                lines.append(f"Dato curioso: {section.curious_fact}")
            lines.append("")
        return "\n".join(lines)
