"""
CEDEAR Screener - Aplicación Principal
API para análisis técnico de CEDEARs basado en acciones subyacentes.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from .config import settings
from .api.routes import router

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
## CEDEAR Screener - Top 5 Diario

Aplicación informativa que calcula diariamente el Top 5 de CEDEARs 
con mayor fortaleza técnica, basada en el análisis de sus acciones 
subyacentes en NASDAQ y NYSE.

### ⚠️ Disclaimer

Este sistema es **exclusivamente informativo y educativo**.  
**No constituye asesoramiento financiero ni recomendación de inversión.**

### Características

- Análisis de indicadores técnicos (RSI, SMA, Volumen, Tendencia)
- Sistema de scoring transparente y explicable
- Datos en tiempo real de acciones subyacentes en USD
- Top 5 CEDEARs actualizados diariamente

### Metodología

Los CEDEARs se ranquean según un sistema de puntos basado en:
- Variación porcentual diaria (+3 pts si > 2%)
- Volumen vs promedio 30 días (+2 pts si superior)
- RSI entre 50-70 (+2 pts)
- Precio sobre SMA 20 (+2 pts)
- Tendencia alcista reciente (+1 pt)
    """,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS para permitir requests desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        # Producción - agregar tu dominio aquí
        "https://*.vercel.app",
        "https://*.netlify.app",
        "https://*.render.com",
    ],
    allow_origin_regex=r"https://.*\.(vercel\.app|netlify\.app|render\.com)$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(router, prefix="/api/v1", tags=["CEDEAR Screener"])


@app.get("/", tags=["Root"])
async def root():
    """
    Endpoint raíz con información básica de la API.
    """
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "API para análisis técnico de CEDEARs",
        "docs": "/docs",
        "disclaimer": (
            "Este sistema es exclusivamente informativo y educativo. "
            "No constituye asesoramiento financiero."
        )
    }


@app.on_event("startup")
async def startup_event():
    """
    Evento de inicio de la aplicación.
    """
    logger.info(f"Iniciando {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info("API disponible en http://localhost:8000")
    logger.info("Documentación disponible en http://localhost:8000/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Evento de cierre de la aplicación.
    """
    logger.info("Cerrando aplicación...")
