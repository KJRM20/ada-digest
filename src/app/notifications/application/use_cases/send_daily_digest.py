from src.app.agent.domain.entities.daily_digest import DailyDigest
from src.app.notifications.application.ports.email_port import EmailPort
from src.app.notifications.application.ports.renderer_port import RendererPort


class SendDailyDigestUseCase:
    def __init__(
        self,
        renderer_port: RendererPort,
        email_port: EmailPort,
    ) -> None:
        self._renderer = renderer_port
        self._email_port = email_port

    def execute(self, digest: DailyDigest) -> None:
        message = self._renderer.render(digest)
        self._email_port.send(message)
