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


# Universo de CEDEARs - Solo los que REALMENTE operan en BYMA
# Lista verificada de CEDEARs disponibles en Argentina
CEDEAR_UNIVERSE: Dict[str, Dict] = {
    # ═══════════════════════════════════════════════════════════════
    # TECNOLOGÍA
    # ═══════════════════════════════════════════════════════════════
    "AAPL": {"company": "Apple Inc.", "ratio": 10},
    "MSFT": {"company": "Microsoft Corporation", "ratio": 5},
    "GOOGL": {"company": "Alphabet Inc. (Google)", "ratio": 29},
    "AMZN": {"company": "Amazon.com Inc.", "ratio": 72},
    "NVDA": {"company": "NVIDIA Corporation", "ratio": 4},
    "META": {"company": "Meta Platforms Inc.", "ratio": 6},
    "NFLX": {"company": "Netflix Inc.", "ratio": 8},
    "AMD": {"company": "Advanced Micro Devices Inc.", "ratio": 5},
    "INTC": {"company": "Intel Corporation", "ratio": 4},
    "CRM": {"company": "Salesforce Inc.", "ratio": 5},
    "ORCL": {"company": "Oracle Corporation", "ratio": 3},
    "CSCO": {"company": "Cisco Systems Inc.", "ratio": 4},
    "IBM": {"company": "IBM Corporation", "ratio": 2},
    "ADBE": {"company": "Adobe Inc.", "ratio": 6},
    "QCOM": {"company": "Qualcomm Inc.", "ratio": 4},
    "TXN": {"company": "Texas Instruments Inc.", "ratio": 3},
    "AVGO": {"company": "Broadcom Inc.", "ratio": 10},
    "MU": {"company": "Micron Technology Inc.", "ratio": 5},
    "PYPL": {"company": "PayPal Holdings Inc.", "ratio": 5},
    "SHOP": {"company": "Shopify Inc.", "ratio": 5},
    "SNAP": {"company": "Snap Inc.", "ratio": 10},
    "UBER": {"company": "Uber Technologies Inc.", "ratio": 5},
    "SPOT": {"company": "Spotify Technology", "ratio": 3},
    "ZM": {"company": "Zoom Video Communications", "ratio": 5},
    "TWLO": {"company": "Twilio Inc.", "ratio": 5},
    "SNOW": {"company": "Snowflake Inc.", "ratio": 5},
    "PLTR": {"company": "Palantir Technologies", "ratio": 10},
    "COIN": {"company": "Coinbase Global Inc.", "ratio": 5},
    "HOOD": {"company": "Robinhood Markets Inc.", "ratio": 10},
    "DOCU": {"company": "DocuSign Inc.", "ratio": 5},
    
    # ═══════════════════════════════════════════════════════════════
    # ARGENTINA / LATAM
    # ═══════════════════════════════════════════════════════════════
    "MELI": {"company": "MercadoLibre Inc.", "ratio": 60},
    "GLOB": {"company": "Globant S.A.", "ratio": 5},
    "VIST": {"company": "Vista Energy", "ratio": 1},
    "NU": {"company": "Nu Holdings (Nubank)", "ratio": 5},
    "STNE": {"company": "StoneCo Ltd.", "ratio": 5},
    "PAGS": {"company": "PagSeguro Digital", "ratio": 5},
    
    # ═══════════════════════════════════════════════════════════════
    # FINANZAS
    # ═══════════════════════════════════════════════════════════════
    "JPM": {"company": "JPMorgan Chase & Co.", "ratio": 4},
    "WFC": {"company": "Wells Fargo & Co.", "ratio": 4},
    "C": {"company": "Citigroup Inc.", "ratio": 4},
    "GS": {"company": "Goldman Sachs Group Inc.", "ratio": 3},
    "V": {"company": "Visa Inc.", "ratio": 4},
    "MA": {"company": "Mastercard Inc.", "ratio": 3},
    "AXP": {"company": "American Express Co.", "ratio": 3},
    "USB": {"company": "U.S. Bancorp", "ratio": 4},
    "BK": {"company": "Bank of New York Mellon", "ratio": 4},
    
    # ═══════════════════════════════════════════════════════════════
    # CONSUMO
    # ═══════════════════════════════════════════════════════════════
    "KO": {"company": "The Coca-Cola Company", "ratio": 5},
    "PEP": {"company": "PepsiCo Inc.", "ratio": 4},
    "WMT": {"company": "Walmart Inc.", "ratio": 5},
    "PG": {"company": "Procter & Gamble Co.", "ratio": 3},
    "COST": {"company": "Costco Wholesale Corp.", "ratio": 4},
    "NKE": {"company": "Nike Inc.", "ratio": 4},
    "SBUX": {"company": "Starbucks Corporation", "ratio": 5},
    "MCD": {"company": "McDonald's Corporation", "ratio": 2},
    "HD": {"company": "The Home Depot Inc.", "ratio": 3},
    "TGT": {"company": "Target Corporation", "ratio": 4},
    "CL": {"company": "Colgate-Palmolive Co.", "ratio": 4},
    "MDLZ": {"company": "Mondelez International", "ratio": 5},
    
    # ═══════════════════════════════════════════════════════════════
    # ENTRETENIMIENTO Y COMUNICACIONES
    # ═══════════════════════════════════════════════════════════════
    "T": {"company": "AT&T Inc.", "ratio": 5},
    "VZ": {"company": "Verizon Communications", "ratio": 4},
    "TMUS": {"company": "T-Mobile US Inc.", "ratio": 3},
    "EA": {"company": "Electronic Arts Inc.", "ratio": 4},
    
    # ═══════════════════════════════════════════════════════════════
    # SALUD Y FARMACÉUTICAS
    # ═══════════════════════════════════════════════════════════════
    "JNJ": {"company": "Johnson & Johnson", "ratio": 3},
    "PFE": {"company": "Pfizer Inc.", "ratio": 5},
    "UNH": {"company": "UnitedHealth Group Inc.", "ratio": 2},
    "ABBV": {"company": "AbbVie Inc.", "ratio": 3},
    "MRK": {"company": "Merck & Co. Inc.", "ratio": 3},
    "LLY": {"company": "Eli Lilly & Co.", "ratio": 2},
    "TMO": {"company": "Thermo Fisher Scientific", "ratio": 2},
    "ABT": {"company": "Abbott Laboratories", "ratio": 4},
    "BMY": {"company": "Bristol-Myers Squibb Co.", "ratio": 4},
    "AMGN": {"company": "Amgen Inc.", "ratio": 2},
    "GILD": {"company": "Gilead Sciences Inc.", "ratio": 4},
    "BIIB": {"company": "Biogen Inc.", "ratio": 3},
    "VRTX": {"company": "Vertex Pharmaceuticals", "ratio": 2},
    "MRNA": {"company": "Moderna Inc.", "ratio": 5},
    "CVS": {"company": "CVS Health Corporation", "ratio": 4},
    "DHR": {"company": "Danaher Corporation", "ratio": 3},
    "ISRG": {"company": "Intuitive Surgical Inc.", "ratio": 3},
    "MDT": {"company": "Medtronic PLC", "ratio": 4},
    
    # ═══════════════════════════════════════════════════════════════
    # INDUSTRIALES
    # ═══════════════════════════════════════════════════════════════
    "BA": {"company": "The Boeing Company", "ratio": 3},
    "CAT": {"company": "Caterpillar Inc.", "ratio": 2},
    "DE": {"company": "Deere & Company", "ratio": 2},
    "GE": {"company": "General Electric Co.", "ratio": 4},
    "HON": {"company": "Honeywell International", "ratio": 2},
    "MMM": {"company": "3M Company", "ratio": 3},
    "UNP": {"company": "Union Pacific Corp.", "ratio": 2},
    "FDX": {"company": "FedEx Corporation", "ratio": 2},
    "LMT": {"company": "Lockheed Martin Corp.", "ratio": 1},
    "RTX": {"company": "RTX Corporation (Raytheon)", "ratio": 3},
    
    # ═══════════════════════════════════════════════════════════════
    # ENERGÍA
    # ═══════════════════════════════════════════════════════════════
    "XOM": {"company": "Exxon Mobil Corporation", "ratio": 3},
    "CVX": {"company": "Chevron Corporation", "ratio": 2},
    "SLB": {"company": "Schlumberger Ltd.", "ratio": 4},
    "OXY": {"company": "Occidental Petroleum", "ratio": 5},
    "HAL": {"company": "Halliburton Company", "ratio": 5},
    "PSX": {"company": "Phillips 66", "ratio": 3},
    
    # ═══════════════════════════════════════════════════════════════
    # MINERÍA Y MATERIALES
    # ═══════════════════════════════════════════════════════════════
    "NUE": {"company": "Nucor Corporation", "ratio": 3},
    "FCX": {"company": "Freeport-McMoRan Inc.", "ratio": 5},
    "NEM": {"company": "Newmont Corporation", "ratio": 4},
    "GOLD": {"company": "Barrick Gold Corporation", "ratio": 5},
    "VALE": {"company": "Vale S.A.", "ratio": 5},
    "RIO": {"company": "Rio Tinto Group", "ratio": 2},
    "BHP": {"company": "BHP Group Limited", "ratio": 3},
    "SCCO": {"company": "Southern Copper Corp.", "ratio": 2},
    "ECL": {"company": "Ecolab Inc.", "ratio": 3},
    "DD": {"company": "DuPont de Nemours Inc.", "ratio": 4},
    "DOW": {"company": "Dow Inc.", "ratio": 4},
    
    # ═══════════════════════════════════════════════════════════════
    # AUTOMOTRIZ Y TRANSPORTE
    # ═══════════════════════════════════════════════════════════════
    "TSLA": {"company": "Tesla Inc.", "ratio": 15},
    "F": {"company": "Ford Motor Company", "ratio": 10},
    "GM": {"company": "General Motors Company", "ratio": 5},
    "TM": {"company": "Toyota Motor Corporation", "ratio": 2},
    "NIO": {"company": "NIO Inc.", "ratio": 10},
    "XPEV": {"company": "XPeng Inc.", "ratio": 10},
    "AAL": {"company": "American Airlines Group", "ratio": 10},
    
    # ═══════════════════════════════════════════════════════════════
    # CHINA / ASIA
    # ═══════════════════════════════════════════════════════════════
    "BABA": {"company": "Alibaba Group Holding Ltd.", "ratio": 9},
    "JD": {"company": "JD.com Inc.", "ratio": 5},
    "PDD": {"company": "PDD Holdings (Pinduoduo)", "ratio": 5},
    "BIDU": {"company": "Baidu Inc.", "ratio": 5},
    "TSM": {"company": "Taiwan Semiconductor", "ratio": 5},
    "SONY": {"company": "Sony Group Corporation", "ratio": 3},
    
    # ═══════════════════════════════════════════════════════════════
    # OTROS
    # ═══════════════════════════════════════════════════════════════
    "ABNB": {"company": "Airbnb Inc.", "ratio": 5},
    "BKNG": {"company": "Booking Holdings Inc.", "ratio": 1},
    "SPGI": {"company": "S&P Global Inc.", "ratio": 2},
    "NOW": {"company": "ServiceNow Inc.", "ratio": 3},
    "ADP": {"company": "Automatic Data Processing", "ratio": 3},
    "LRCX": {"company": "Lam Research Corp.", "ratio": 2},
    "AMAT": {"company": "Applied Materials Inc.", "ratio": 4},
    "ADI": {"company": "Analog Devices Inc.", "ratio": 3},
    "MRVL": {"company": "Marvell Technology Inc.", "ratio": 5},
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
