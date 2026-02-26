from src.app.notifications.application.use_cases.send_daily_digest import (
    SendDailyDigestUseCase,
)
from src.app.notifications.infrastructure.driving_adapters.config.dependencies.gmail_config import (
    get_gmail_adapter,
)
from src.app.notifications.infrastructure.driving_adapters.config.dependencies.jinja_config import (
    get_jinja_renderer,
)


def get_send_daily_digest_use_case() -> SendDailyDigestUseCase:
    return SendDailyDigestUseCase(
        renderer_port=get_jinja_renderer(),
        email_port=get_gmail_adapter(),
    )
