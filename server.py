"""FastAPI server con scheduler en background.

Este servidor expone un endpoint HTTP /health para health checks
mientras ejecuta el scheduler de digest en un thread background.

Diseñado para deployment en Render Free Tier, donde el servidor
debe responder HTTP requests para evitar que la instancia "duerma".
"""

import logging
import threading

from dotenv import load_dotenv
from fastapi import FastAPI

# Cargar variables de entorno antes de imports internos
load_dotenv()

from src.app.agent.infrastructure.driving_adapters.config.dependencies.scheduler_config import (
    get_digest_scheduler,
)
from src.app.agent.infrastructure.driving_adapters.health.health_router import (
    router as health_router,
)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Crear app FastAPI
app = FastAPI(
    title="Ada Scheduler API",
    description="API para el scheduler de digest de Ada con health check",
    version="1.0.0",
)

# Montar el router de health
app.include_router(health_router)


def start_scheduler() -> None:
    """Inicia el scheduler de digest en el thread actual.

    Esta función se ejecuta en un thread background daemon,
    permitiendo que FastAPI responda requests HTTP mientras
    el scheduler procesa los jobs programados.
    """
    try:
        logger.info("🚀 Iniciando scheduler de digest en background thread...")
        scheduler = get_digest_scheduler()
        scheduler.start()
    except Exception as e:
        logger.error(f"❌ Error en scheduler: {e}", exc_info=True)


# Iniciar scheduler en thread background al importar este módulo
scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
scheduler_thread.start()
logger.info("✅ Scheduler thread iniciado")


@app.on_event("startup")
async def startup_event() -> None:
    """Log de inicio del servidor."""
    logger.info("✨ FastAPI server iniciado - Ready to receive requests")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Log de cierre del servidor."""
    logger.info("👋 FastAPI server detenido")


@app.get("/")
async def root() -> dict[str, str | dict[str, str]]:
    """Root endpoint con información del servicio."""
    return {
        "service": "Ada Scheduler API",
        "description": "Servicio de digest diario para programadores",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "redoc": "/redoc",
        },
    }
