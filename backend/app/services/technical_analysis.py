"""
Servicio de cálculo de indicadores técnicos.
Calcula RSI, SMA, tendencia y otros indicadores sobre datos de mercado.
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional, Literal
import logging

from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator
from typing import Optional

from ..config import TECHNICAL_PARAMS
from ..models import StockIndicators

logger = logging.getLogger(__name__)


class TechnicalAnalysisService:
    """
    Servicio para calcular indicadores técnicos sobre datos de precios.
    """
    
    def __init__(self):
        self.rsi_period = TECHNICAL_PARAMS["rsi_period"]
        self.sma_period = TECHNICAL_PARAMS["sma_period"]
        self.volume_ma_period = TECHNICAL_PARAMS["volume_ma_period"]
        self.trend_lookback = TECHNICAL_PARAMS["trend_lookback"]
    
    def calculate_rsi(self, df: pd.DataFrame) -> pd.Series:
        """
        Calcula el RSI (Relative Strength Index).
        
        Args:
            df: DataFrame con columna 'Close'
            
        Returns:
            Serie con valores RSI
        """
        rsi = RSIIndicator(close=df["Close"], window=self.rsi_period)
        return rsi.rsi()
    
    def calculate_sma(self, df: pd.DataFrame, period: Optional[int] = None) -> pd.Series:
        """
        Calcula la media móvil simple (SMA).
        
        Args:
            df: DataFrame con columna 'Close'
            period: Período de la media móvil
            
        Returns:
            Serie con valores SMA
        """
        period = period or self.sma_period
        sma = SMAIndicator(close=df["Close"], window=period)
        return sma.sma_indicator()
    
    def calculate_volume_ma(self, df: pd.DataFrame) -> pd.Series:
        """
        Calcula la media móvil del volumen.
        
        Args:
            df: DataFrame con columna 'Volume'
            
        Returns:
            Serie con promedio móvil de volumen
        """
        return df["Volume"].rolling(window=self.volume_ma_period).mean()
    
    def determine_trend(
        self, 
        df: pd.DataFrame, 
        lookback: Optional[int] = None
    ) -> Literal["bullish", "bearish", "neutral"]:
        """
        Determina la tendencia reciente basada en los últimos N días.
        
        Criterio:
        - Bullish: El precio subió más del 2% en el período
        - Bearish: El precio bajó más del 2% en el período
        - Neutral: Cambio menor al 2%
        
        Args:
            df: DataFrame con columna 'Close'
            lookback: Días a considerar para la tendencia
            
        Returns:
            "bullish", "bearish" o "neutral"
        """
        lookback = lookback or self.trend_lookback
        
        if len(df) < lookback:
            return "neutral"
        
        recent_prices = df["Close"].tail(lookback)
        start_price = recent_prices.iloc[0]
        end_price = recent_prices.iloc[-1]
        
        change_pct = ((end_price - start_price) / start_price) * 100
        
        if change_pct > 2:
            return "bullish"
        elif change_pct < -2:
            return "bearish"
        else:
            return "neutral"
    
    def calculate_daily_change(self, df: pd.DataFrame) -> float:
        """
        Calcula la variación porcentual diaria.
        
        Args:
            df: DataFrame con columna 'Close'
            
        Returns:
            Variación porcentual del último día
        """
        if len(df) < 2:
            return 0.0
        
        today_close = df["Close"].iloc[-1]
        yesterday_close = df["Close"].iloc[-2]
        
        return ((today_close - yesterday_close) / yesterday_close) * 100
    
    def calculate_all_indicators(
        self, 
        ticker: str, 
        df: pd.DataFrame
    ) -> Optional[StockIndicators]:
        """
        Calcula todos los indicadores técnicos para una acción.
        
        Args:
            ticker: Símbolo de la acción
            df: DataFrame con datos históricos (OHLCV)
            
        Returns:
            StockIndicators con todos los indicadores calculados
        """
        try:
            if df is None or len(df) < self.volume_ma_period:
                logger.warning(
                    f"Datos insuficientes para {ticker}: "
                    f"{len(df) if df is not None else 0} filas"
                )
                return None
            
            # Precio actual
            current_price = float(df["Close"].iloc[-1])
            
            # Variación diaria
            daily_change_pct = self.calculate_daily_change(df)
            
            # Volumen
            current_volume = int(df["Volume"].iloc[-1])
            volume_ma = self.calculate_volume_ma(df)
            volume_avg_30d = float(volume_ma.iloc[-1]) if not pd.isna(volume_ma.iloc[-1]) else 0
            volume_ratio = (
                current_volume / volume_avg_30d if volume_avg_30d > 0 else 1.0
            )
            
            # RSI
            rsi_series = self.calculate_rsi(df)
            rsi = float(rsi_series.iloc[-1]) if not pd.isna(rsi_series.iloc[-1]) else 50.0
            
            # SMA 20
            sma_series = self.calculate_sma(df)
            sma_20 = float(sma_series.iloc[-1]) if not pd.isna(sma_series.iloc[-1]) else current_price
            above_sma = current_price > sma_20
            
            # Tendencia
            trend = self.determine_trend(df)
            
            return StockIndicators(
                ticker=ticker,
                current_price=round(current_price, 2),
                daily_change_pct=round(daily_change_pct, 2),
                volume=current_volume,
                volume_avg_30d=round(volume_avg_30d, 0),
                volume_ratio=round(volume_ratio, 2),
                rsi=round(rsi, 2),
                sma_20=round(sma_20, 2),
                above_sma=above_sma,
                trend=trend
            )
            
        except Exception as e:
            logger.error(f"Error calculando indicadores para {ticker}: {str(e)}")
            return None
    
    def analyze_multiple_stocks(
        self, 
        stocks_data: Dict[str, pd.DataFrame]
    ) -> Dict[str, StockIndicators]:
        """
        Calcula indicadores para múltiples acciones.
        
        Args:
            stocks_data: Diccionario {ticker: DataFrame}
            
        Returns:
            Diccionario {ticker: StockIndicators}
        """
        results = {}
        
        for ticker, df in stocks_data.items():
            indicators = self.calculate_all_indicators(ticker, df)
            if indicators is not None:
                results[ticker] = indicators
        
        logger.info(f"Indicadores calculados para {len(results)} acciones")
        return results


# Instancia global del servicio
technical_analysis_service = TechnicalAnalysisService()
