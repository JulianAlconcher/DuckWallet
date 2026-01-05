"""
Servicio de obtención de datos de mercado.
Utiliza yfinance como fuente principal de datos.
"""

import yfinance as yf
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging

from ..config import CEDEAR_UNIVERSE, TECHNICAL_PARAMS

logger = logging.getLogger(__name__)


class MarketDataService:
    """
    Servicio para obtener datos de mercado de acciones subyacentes.
    Utiliza yfinance para obtener datos históricos y en tiempo real.
    """
    
    def __init__(self):
        self.cache: Dict[str, pd.DataFrame] = {}
        self.cache_timestamp: Optional[datetime] = None
        self.cache_ttl = timedelta(minutes=15)  # Cache de 15 minutos
    
    def _is_cache_valid(self) -> bool:
        """Verifica si el cache es válido."""
        if self.cache_timestamp is None:
            return False
        return datetime.now() - self.cache_timestamp < self.cache_ttl
    
    def get_stock_history(
        self, 
        ticker: str, 
        period_days: int = 60
    ) -> Optional[pd.DataFrame]:
        """
        Obtiene el historial de precios de una acción.
        
        Args:
            ticker: Símbolo de la acción (ej: "AAPL")
            period_days: Días de historia a obtener
            
        Returns:
            DataFrame con columnas: Open, High, Low, Close, Volume, Adj Close
        """
        try:
            stock = yf.Ticker(ticker)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=period_days)
            
            df = stock.history(start=start_date, end=end_date)
            
            if df.empty:
                logger.warning(f"No se obtuvieron datos para {ticker}")
                return None
            
            return df
            
        except Exception as e:
            logger.error(f"Error obteniendo datos de {ticker}: {str(e)}")
            return None
    
    def get_all_stocks_data(
        self, 
        tickers: Optional[List[str]] = None
    ) -> Dict[str, pd.DataFrame]:
        """
        Obtiene datos históricos de múltiples acciones.
        
        Args:
            tickers: Lista de tickers. Si es None, usa el universo completo.
            
        Returns:
            Diccionario {ticker: DataFrame}
        """
        if tickers is None:
            tickers = list(CEDEAR_UNIVERSE.keys())
        
        # Verificar cache
        if self._is_cache_valid() and set(tickers).issubset(set(self.cache.keys())):
            logger.info("Usando datos desde cache")
            return {t: self.cache[t] for t in tickers}
        
        result = {}
        period_days = TECHNICAL_PARAMS["history_days"]
        
        # Descargar datos en batch para mejor rendimiento
        tickers_str = " ".join(tickers)
        logger.info(f"Descargando datos de: {tickers_str}")
        
        try:
            # Usar download para obtener múltiples tickers a la vez
            data = yf.download(
                tickers_str,
                period=f"{period_days}d",
                group_by='ticker',
                progress=False,
                threads=True
            )
            
            if len(tickers) == 1:
                # Si es un solo ticker, el formato es diferente
                if not data.empty:
                    result[tickers[0]] = data
            else:
                # Múltiples tickers
                for ticker in tickers:
                    if ticker in data.columns.get_level_values(0):
                        ticker_data = data[ticker].dropna()
                        if not ticker_data.empty:
                            result[ticker] = ticker_data
                        else:
                            logger.warning(f"Datos vacíos para {ticker}")
                    else:
                        logger.warning(f"No se encontró {ticker} en los datos")
                        
        except Exception as e:
            logger.error(f"Error en descarga batch: {str(e)}")
            # Fallback: descargar uno por uno
            for ticker in tickers:
                df = self.get_stock_history(ticker, period_days)
                if df is not None:
                    result[ticker] = df
        
        # Actualizar cache
        self.cache.update(result)
        self.cache_timestamp = datetime.now()
        
        logger.info(f"Datos obtenidos para {len(result)}/{len(tickers)} tickers")
        return result
    
    def get_current_quote(self, ticker: str) -> Optional[Dict]:
        """
        Obtiene la cotización actual de una acción.
        
        Args:
            ticker: Símbolo de la acción
            
        Returns:
            Diccionario con datos actuales
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            return {
                "symbol": ticker,
                "price": info.get("regularMarketPrice", 0),
                "previous_close": info.get("regularMarketPreviousClose", 0),
                "volume": info.get("regularMarketVolume", 0),
                "market_cap": info.get("marketCap", 0),
            }
        except Exception as e:
            logger.error(f"Error obteniendo quote de {ticker}: {str(e)}")
            return None


# Instancia global del servicio
market_data_service = MarketDataService()
