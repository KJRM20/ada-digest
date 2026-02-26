"""Adaptador de envío de correo vía simplegmail.

Soporta dos modos de carga de credenciales OAuth:

1. **Archivos en disco** (desarrollo local):
   Usa GMAIL_CLIENT_SECRET_PATH y GMAIL_TOKEN_PATH apuntando
   a archivos JSON en .secrets/.

2. **Variables de entorno con JSON completo** (producción/Render):
   Usa GMAIL_CLIENT_SECRET_JSON y GMAIL_TOKEN_JSON con el
   contenido íntegro del JSON. El adapter materializa archivos
   temporales para que simplegmail pueda leerlos.
"""

import json
import logging
import os
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


def _materialize_json_env_var(env_var: str, suffix: str) -> str | None:
    """Escribe el JSON de una env var a un archivo temporal.

    Args:
        env_var: Nombre de la variable de entorno con JSON.
        suffix: Sufijo para el archivo temporal.

    Returns:
        Ruta al archivo temporal, o None si la env var no existe.
    """
    raw = os.environ.get(env_var)
    if not raw:
        return None

    try:
        json.loads(raw)
    except json.JSONDecodeError:
        logger.error("La variable %s no contiene JSON válido.", env_var)
        return None

    tmp = tempfile.NamedTemporaryFile(
        mode="w",
        suffix=suffix,
        delete=False,
    )
    tmp.write(raw)
    tmp.close()
    logger.info("Secreto %s materializado en %s", env_var, tmp.name)
    return tmp.name


class SimplegmailAdapter:
    """Driven adapter para envío de correo con Gmail."""

    def __init__(self) -> None:
        secret_path = self._resolve_secret_path()
        token_path = self._resolve_token_path()

        self._sender = os.environ["GMAIL_SENDER"]
        self._gmail = Gmail(
            client_secret_file=secret_path,
            creds_file=token_path,
        )

    @staticmethod
    def _resolve_secret_path() -> str:
        """Resuelve la ruta al client secret.

        Prioridad:
        1. GMAIL_CLIENT_SECRET_JSON (env var con JSON completo)
        2. GMAIL_CLIENT_SECRET_PATH (ruta a archivo)
        3. Default: .secrets/client_secret.json
        """
        from_json = _materialize_json_env_var(
            "GMAIL_CLIENT_SECRET_JSON", "_client_secret.json"
        )
        if from_json:
            return from_json

        return os.environ.get("GMAIL_CLIENT_SECRET_PATH", _DEFAULT_SECRET)

    @staticmethod
    def _resolve_token_path() -> str:
        """Resuelve la ruta al token de Gmail.

        Prioridad:
        1. GMAIL_TOKEN_JSON (env var con JSON completo)
        2. GMAIL_TOKEN_PATH (ruta a archivo)
        3. Default: .secrets/gmail-token.json
        """
        from_json = _materialize_json_env_var(
            "GMAIL_TOKEN_JSON", "_gmail_token.json"
        )
        if from_json:
            return from_json

        return os.environ.get("GMAIL_TOKEN_PATH", _DEFAULT_TOKEN)

    def send(self, message: EmailMessage) -> None:
        """Envía un mensaje de correo vía Gmail."""
        self._gmail.send_message(
            to=message.recipient,
            sender=self._sender,
            subject=message.subject,
            msg_html=message.html_body,
            msg_plain=message.plain_body,
        )
