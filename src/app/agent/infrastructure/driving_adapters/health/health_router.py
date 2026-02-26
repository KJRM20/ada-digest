"""Health check router.

Este driving adapter expone un endpoint HTTP simple para
verificar el estado del servicio.
"""

from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint.

    Retorna el estado del servicio y timestamp actual.
    Usado por Render para health checks y por monitores externos
    como UptimeRobot para mantener el servicio activo.

    Returns:
        dict: Estado del servicio y metadata.
    """
    return {
        "status": "ok",
        "service": "ada-scheduler",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
