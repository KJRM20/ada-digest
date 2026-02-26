import os
import time
from datetime import datetime
from zoneinfo import ZoneInfo

import schedule

from src.app.agent.application.use_cases.generate_daily_digest import (
    GenerateDailyDigestUseCase,
)
from src.app.notifications.application.use_cases.send_daily_digest import (
    SendDailyDigestUseCase,
)

_DEFAULT_MORNING = "08:00"
_DEFAULT_EVENING = "20:00"
_DEFAULT_TZ = "America/Bogota"
_POLL_INTERVAL_SECONDS = 30


class DigestScheduler:
    def __init__(
        self,
        generate_uc: GenerateDailyDigestUseCase,
        send_uc: SendDailyDigestUseCase,
    ) -> None:
        self._generate_uc = generate_uc
        self._send_uc = send_uc
        self._tz = ZoneInfo(os.environ.get("DIGEST_TIMEZONE", _DEFAULT_TZ))
        self._morning = os.environ.get("MORNING_DIGEST_TIME", _DEFAULT_MORNING)
        self._evening = os.environ.get("EVENING_DIGEST_TIME", _DEFAULT_EVENING)

    def _run_digest(self) -> None:
        now = datetime.now(self._tz).strftime("%Y-%m-%d %H:%M")
        print(f"[{now}] Generando digest...")
        try:
            digest = self._generate_uc.execute()
            self._send_uc.execute(digest)
            print(f"[{now}] Digest enviado correctamente.")
        except Exception as exc:
            print(f"[{now}] Error al generar/enviar digest: {exc}")

    def run_once(self) -> None:
        """Execute the digest pipeline a single time (for testing)."""
        self._run_digest()

    def start(self) -> None:
        """Register scheduled jobs and enter the polling loop."""
        schedule.every().day.at(self._morning, str(self._tz)).do(
            self._run_digest
        )
        schedule.every().day.at(self._evening, str(self._tz)).do(
            self._run_digest
        )

        print(
            f"Scheduler activo — digest a las {self._morning} "
            f"y {self._evening} ({self._tz})"
        )
        print(
            "Próximo job:",
            schedule.next_run().strftime("%Y-%m-%d %H:%M"),  # type: ignore[union-attr]
        )

        while True:
            schedule.run_pending()
            time.sleep(_POLL_INTERVAL_SECONDS)
