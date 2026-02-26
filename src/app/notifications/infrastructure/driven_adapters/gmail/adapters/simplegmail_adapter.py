"""Adaptador de envío de correo vía simplegmail.

Carga credenciales OAuth desde archivos en disco:

- **Desarrollo local:** .secrets/client_secret.json y .secrets/gmail-token.json
- **Producción (Render):** /etc/secrets/client_secret.json y
  /etc/secrets/gmail-token.json (Secret Files de Render)

Las rutas se configuran vía GMAIL_CLIENT_SECRET_PATH y GMAIL_TOKEN_PATH.
"""

import logging
import os
from pathlib import Path

from simplegmail import Gmail

from src.app.notifications.domain.value_objects.email_message import (
    EmailMessage,
)

logger = logging.getLogger(__name__)

_DEFAULT_SECRET = str(
    Path(__file__).parents[6] / ".secrets" / "client_secret.json"
)
_DEFAULT_TOKEN = str(
    Path(__file__).parents[6] / ".secrets" / "gmail-token.json"
)


class SimplegmailAdapter:
    """Driven adapter para envío de correo con Gmail."""

    def __init__(self) -> None:
        secret_path = os.environ.get(
            "GMAIL_CLIENT_SECRET_PATH", _DEFAULT_SECRET
        )
        token_path = os.environ.get("GMAIL_TOKEN_PATH", _DEFAULT_TOKEN)

        logger.info(
            "Gmail credentials: secret=%s, token=%s",
            secret_path,
            token_path,
        )

        self._sender = os.environ["GMAIL_SENDER"]
        self._gmail = Gmail(
            client_secret_file=secret_path,
            creds_file=token_path,
        )

    def send(self, message: EmailMessage) -> None:
        """Envía un mensaje de correo vía Gmail."""
        self._gmail.send_message(
            to=message.recipient,
            sender=self._sender,
            subject=message.subject,
            msg_html=message.html_body,
            msg_plain=message.plain_body,
        )
