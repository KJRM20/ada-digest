from src.app.agent.infrastructure.driving_adapters.config.dependencies.generate_daily_digest_config import (
    get_generate_daily_digest_use_case,
)
from src.app.agent.infrastructure.driving_adapters.scheduler.digest_scheduler import (
    DigestScheduler,
)
from src.app.notifications.infrastructure.driving_adapters.config.dependencies.send_daily_digest_config import (
    get_send_daily_digest_use_case,
)


def get_digest_scheduler() -> DigestScheduler:
    return DigestScheduler(
        generate_uc=get_generate_daily_digest_use_case(),
        send_uc=get_send_daily_digest_use_case(),
    )
