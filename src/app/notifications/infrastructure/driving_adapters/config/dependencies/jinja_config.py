from src.app.notifications.infrastructure.driven_adapters.gmail.adapters.jinja_renderer_adapter import (
    JinjaRendererAdapter,
)


def get_jinja_renderer() -> JinjaRendererAdapter:
    return JinjaRendererAdapter()
