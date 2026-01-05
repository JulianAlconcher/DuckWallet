"""
Modelos de datos para el CEDEAR Screener.
Define las estructuras de datos utilizadas en la API.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import date


class StockIndicators(BaseModel):
    """Indicadores técnicos calculados para una acción."""
    
    ticker: str = Field(..., description="Símbolo de la acción subyacente")
    current_price: float = Field(..., description="Precio de cierre actual en USD")
    daily_change_pct: float = Field(..., description="Variación porcentual diaria")
    volume: int = Field(..., description="Volumen del día")
    volume_avg_30d: float = Field(..., description="Promedio de volumen 30 días")
    volume_ratio: float = Field(..., description="Ratio volumen actual / promedio")
    rsi: float = Field(..., description="RSI de 14 períodos")
    sma_20: float = Field(..., description="Media móvil simple 20 períodos")
    above_sma: bool = Field(..., description="Precio está por encima de SMA 20")
    trend: Literal["bullish", "bearish", "neutral"] = Field(
        ..., description="Tendencia reciente"
    )


class CEDEARScore(BaseModel):
    """Score técnico de un CEDEAR."""
    
    cedear: str = Field(..., description="Símbolo del CEDEAR (igual al subyacente)")
    company: str = Field(..., description="Nombre de la empresa")
    score: int = Field(..., ge=0, le=10, description="Puntaje técnico (0-10)")
    daily_change_pct: float = Field(..., description="Variación porcentual diaria")
    volume_ratio: float = Field(..., description="Ratio de volumen")
    rsi: float = Field(..., description="RSI actual")
    trend: Literal["bullish", "bearish", "neutral"] = Field(..., description="Tendencia")
    current_price: float = Field(..., description="Precio actual USD")
    price_ars: Optional[float] = Field(None, description="Precio CEDEAR en ARS")
    daily_change_pct_ars: Optional[float] = Field(None, description="Variación porcentual diaria en ARS")
    
    # Detalle del scoring (opcional, para transparencia)
    score_breakdown: Optional[dict] = Field(
        None, description="Desglose del puntaje por criterio"
    )


class Top5Response(BaseModel):
    """Respuesta del endpoint Top 5 CEDEARs."""
    
    date: str = Field(..., description="Fecha del análisis (YYYY-MM-DD)")
    disclaimer: str = Field(
        default="Este análisis es informativo y educativo. No constituye asesoramiento financiero ni recomendación de inversión.",
        description="Disclaimer legal"
    )
    top5: List[CEDEARScore] = Field(..., description="Top 5 CEDEARs por score técnico")
    
    class Config:
        json_schema_extra = {
            "example": {
                "date": "2024-01-15",
                "disclaimer": "Este análisis es informativo y educativo...",
                "top5": [
                    {
                        "cedear": "AAPL",
                        "company": "Apple Inc.",
                        "score": 8,
                        "daily_change_pct": 2.3,
                        "volume_ratio": 1.5,
                        "rsi": 61,
                        "trend": "bullish",
                        "current_price": 185.50,
                    }
                ]
            }
        }


class HealthResponse(BaseModel):
    """Respuesta del endpoint de health check."""
    
    status: str = Field(..., description="Estado del servicio")
    version: str = Field(..., description="Versión de la API")


class AllCEDEARSResponse(BaseModel):
    """Respuesta con todos los CEDEARs analizados."""
    
    date: str = Field(..., description="Fecha del análisis")
    disclaimer: str = Field(
        default="Este análisis es informativo y educativo. No constituye asesoramiento financiero ni recomendación de inversión."
    )
    total: int = Field(..., description="Total de CEDEARs analizados")
    cedears: List[CEDEARScore] = Field(..., description="Lista completa ordenada por score")
