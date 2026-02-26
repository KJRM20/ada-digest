"""Adaptador de envío de correo vía simplegmail.

Carga credenciales OAuth desde archivos en disco:

- **Desarrollo local:** .secrets/client_secret.json y
  .secrets/gmail-token.json
- **Producción (Render):** /etc/secrets/ (Secret Files montados
  como symlinks, se copian a /tmp para compatibilidad con
  oauth2client).

Las rutas se configuran vía GMAIL_CLIENT_SECRET_PATH y
GMAIL_TOKEN_PATH.
"""

import logging
import os
import shutil
import tempfile
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


def _resolve_path(path: str) -> str:
    """Copy symlinked files to /tmp so oauth2client accepts them."""
    if os.path.islink(path):
        suffix = Path(path).suffix
        tmp = tempfile.NamedTemporaryFile(
            delete=False, suffix=suffix, prefix="gmail_"
        )
        shutil.copy2(path, tmp.name)
        logger.info("Copied symlink %s → %s", path, tmp.name)
        return tmp.name
    return path


class SimplegmailAdapter:
    """Driven adapter para envío de correo con Gmail."""

    def __init__(self) -> None:
        secret_path = os.environ.get(
            "GMAIL_CLIENT_SECRET_PATH", _DEFAULT_SECRET
        )
        token_path = os.environ.get("GMAIL_TOKEN_PATH", _DEFAULT_TOKEN)

        # Resolve symlinks (Render Secret Files)
        secret_path = _resolve_path(secret_path)
        token_path = _resolve_path(token_path)

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
