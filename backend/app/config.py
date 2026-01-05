"""
Configuración del CEDEAR Screener.
Define el universo de activos y parámetros del sistema de scoring.
"""

from pydantic_settings import BaseSettings
from typing import Dict, List
import os


class Settings(BaseSettings):
    """Configuración de la aplicación."""
    
    # API Keys
    ALPHA_VANTAGE_API_KEY: str = os.getenv("ALPHA_VANTAGE_API_KEY", "")
    
    # Configuración del servidor
    APP_NAME: str = "CEDEAR Screener"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"


# Universo de CEDEARs - Mapeo: Ticker subyacente -> Información del CEDEAR
CEDEAR_UNIVERSE: Dict[str, Dict] = {
    "AAPL": {"company": "Apple Inc.", "ratio": 10},
    "MSFT": {"company": "Microsoft Corporation", "ratio": 5},
    "GOOGL": {"company": "Alphabet Inc.", "ratio": 29},
    "AMZN": {"company": "Amazon.com Inc.", "ratio": 72},
    "TSLA": {"company": "Tesla Inc.", "ratio": 15},
    "NVDA": {"company": "NVIDIA Corporation", "ratio": 4},
    "META": {"company": "Meta Platforms Inc.", "ratio": 6},
    "KO": {"company": "The Coca-Cola Company", "ratio": 5},
    "JNJ": {"company": "Johnson & Johnson", "ratio": 3},
    "JPM": {"company": "JPMorgan Chase & Co.", "ratio": 4},
    "V": {"company": "Visa Inc.", "ratio": 4},
    "DIS": {"company": "The Walt Disney Company", "ratio": 4},
    "NFLX": {"company": "Netflix Inc.", "ratio": 8},
    "AMD": {"company": "Advanced Micro Devices Inc.", "ratio": 5},
    "INTC": {"company": "Intel Corporation", "ratio": 4},
    "PEP": {"company": "PepsiCo Inc.", "ratio": 4},
    "WMT": {"company": "Walmart Inc.", "ratio": 5},
    "BA": {"company": "The Boeing Company", "ratio": 3},
    "GS": {"company": "Goldman Sachs Group Inc.", "ratio": 3},
    "BABA": {"company": "Alibaba Group Holding Ltd.", "ratio": 9},
}


# Parámetros para indicadores técnicos
TECHNICAL_PARAMS = {
    "rsi_period": 14,
    "sma_period": 20,
    "volume_ma_period": 30,
    "trend_lookback": 5,
    "history_days": 60,  # Días de historia para calcular indicadores
}


# Sistema de Scoring - Reglas y puntajes
SCORING_RULES = {
    "daily_change_threshold": 2.0,      # Umbral de variación diaria (%)
    "daily_change_points": 3,           # Puntos si supera el umbral
    
    "volume_above_avg_points": 2,       # Puntos si volumen > promedio
    
    "rsi_min": 50,                      # RSI mínimo para zona óptima
    "rsi_max": 70,                      # RSI máximo para zona óptima
    "rsi_optimal_points": 2,            # Puntos si RSI en zona óptima
    
    "above_sma_points": 2,              # Puntos si precio > SMA
    
    "bullish_trend_points": 1,          # Puntos si tendencia alcista
}


# Configuración de API de datos
DATA_SOURCES = {
    "primary": "yfinance",    # Usar yfinance como fuente principal (gratuito)
    "fallback": "alpha_vantage",
}


settings = Settings()
