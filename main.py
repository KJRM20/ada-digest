import sys

from dotenv import load_dotenv

load_dotenv()

from src.app.agent.infrastructure.driving_adapters.config.dependencies.scheduler_config import (
    get_digest_scheduler,
)


def main() -> None:
    scheduler = get_digest_scheduler()

    if "--once" in sys.argv:
        scheduler.run_once()
    else:
        scheduler.start()


if __name__ == "__main__":
    main()
