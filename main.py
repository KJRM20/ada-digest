from dotenv import load_dotenv

load_dotenv()

from src.app.agent.infrastructure.driving_adapters.config.dependencies.generate_daily_digest_config import (
    get_generate_daily_digest_use_case,
)
from src.app.notifications.infrastructure.driving_adapters.config.dependencies.send_daily_digest_config import (
    get_send_daily_digest_use_case,
)


def main() -> None:
    digest = get_generate_daily_digest_use_case().execute()
    get_send_daily_digest_use_case().execute(digest)
    print("Digest enviado correctamente.")


if __name__ == "__main__":
    main()
