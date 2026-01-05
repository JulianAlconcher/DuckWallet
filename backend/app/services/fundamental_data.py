"""
Servicio de obtención de datos fundamentales.
Obtiene métricas de valuación y calidad para estrategia Value.
"""

import yfinance as yf
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging

from ..config import CEDEAR_UNIVERSE

logger = logging.getLogger(__name__)


class FundamentalDataService:
    """
    Servicio para obtener datos fundamentales de acciones.
    Métricas de valuación, calidad y crecimiento.
    """
    
    def __init__(self):
        self.cache: Dict[str, Dict] = {}
        self.cache_timestamp: Optional[datetime] = None
        self.cache_ttl = timedelta(hours=1)  # Cache de 1 hora (fundamentales cambian menos)
    
    def _is_cache_valid(self) -> bool:
        """Verifica si el cache es válido."""
        if self.cache_timestamp is None:
            return False
        return datetime.now() - self.cache_timestamp < self.cache_ttl
    
    def get_fundamentals(self, ticker: str) -> Optional[Dict]:
        """
        Obtiene datos fundamentales de una acción.
        
        Args:
            ticker: Símbolo de la acción
            
        Returns:
            Diccionario con métricas fundamentales
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            return {
                "ticker": ticker,
                # Valuación
                "pe_ratio": info.get("trailingPE"),
                "forward_pe": info.get("forwardPE"),
                "price_to_book": info.get("priceToBook"),
                "price_to_sales": info.get("priceToSalesTrailing12Months"),
                # Dividendos
                "dividend_yield": info.get("dividendYield"),
                # Calidad
                "roe": info.get("returnOnEquity"),
                "profit_margin": info.get("profitMargins"),
                "debt_to_equity": info.get("debtToEquity"),
                "current_ratio": info.get("currentRatio"),
                # Crecimiento
                "earnings_growth": info.get("earningsGrowth"),
                "revenue_growth": info.get("revenueGrowth"),
                # Info adicional
                "market_cap": info.get("marketCap"),
                "sector": info.get("sector"),
            }
        except Exception as e:
            logger.error(f"Error obteniendo fundamentales de {ticker}: {str(e)}")
            return None
    
    def get_all_fundamentals(
        self, 
        tickers: Optional[List[str]] = None
    ) -> Dict[str, Dict]:
        """
        Obtiene datos fundamentales de múltiples acciones.
        
        Args:
            tickers: Lista de tickers. Si es None, usa el universo completo.
            
        Returns:
            Diccionario {ticker: fundamentals}
        """
        if tickers is None:
            tickers = list(CEDEAR_UNIVERSE.keys())
        
        # Verificar cache
        if self._is_cache_valid() and set(tickers).issubset(set(self.cache.keys())):
            logger.info("Usando fundamentales desde cache")
            return {t: self.cache[t] for t in tickers if t in self.cache}
        
        result = {}
        logger.info(f"Obteniendo fundamentales de {len(tickers)} acciones...")
        
        for ticker in tickers:
            fundamentals = self.get_fundamentals(ticker)
            if fundamentals:
                result[ticker] = fundamentals
        
        # Actualizar cache
        self.cache.update(result)
        self.cache_timestamp = datetime.now()
        
        logger.info(f"Fundamentales obtenidos para {len(result)}/{len(tickers)} tickers")
        return result


# Instancia global del servicio
fundamental_data_service = FundamentalDataService()
