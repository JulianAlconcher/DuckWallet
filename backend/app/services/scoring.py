"""
Servicio de scoring para CEDEARs.
Calcula el puntaje técnico basado en reglas explícitas y transparentes.
"""

from typing import Dict, List
import logging

from ..config import CEDEAR_UNIVERSE, SCORING_RULES
from ..models import StockIndicators, CEDEARScore

logger = logging.getLogger(__name__)


class ScoringService:
    """
    Servicio para calcular el score técnico de cada CEDEAR.
    Implementa un sistema de puntos basado en reglas claras y explicables.
    """
    
    def __init__(self):
        self.rules = SCORING_RULES
        self.universe = CEDEAR_UNIVERSE
    
    def calculate_score(self, indicators: StockIndicators) -> Dict:
        """
        Calcula el score técnico para una acción basado en sus indicadores.
        
        Sistema de puntuación:
        - +3 puntos: Variación diaria > 2%
        - +2 puntos: Volumen > promedio 30 días
        - +2 puntos: RSI entre 50 y 70 (zona óptima)
        - +2 puntos: Precio > SMA 20
        - +1 punto: Tendencia alcista reciente
        
        Máximo: 10 puntos
        
        Args:
            indicators: Indicadores técnicos calculados
            
        Returns:
            Diccionario con score total y desglose
        """
        score = 0
        breakdown = {}
        
        # Regla 1: Variación diaria significativa
        if indicators.daily_change_pct > self.rules["daily_change_threshold"]:
            points = self.rules["daily_change_points"]
            score += points
            breakdown["daily_change"] = {
                "points": points,
                "reason": f"Variación diaria {indicators.daily_change_pct:.2f}% > {self.rules['daily_change_threshold']}%"
            }
        else:
            breakdown["daily_change"] = {
                "points": 0,
                "reason": f"Variación diaria {indicators.daily_change_pct:.2f}% <= {self.rules['daily_change_threshold']}%"
            }
        
        # Regla 2: Volumen superior al promedio
        if indicators.volume_ratio > 1.0:
            points = self.rules["volume_above_avg_points"]
            score += points
            breakdown["volume"] = {
                "points": points,
                "reason": f"Volumen {indicators.volume_ratio:.2f}x el promedio"
            }
        else:
            breakdown["volume"] = {
                "points": 0,
                "reason": f"Volumen {indicators.volume_ratio:.2f}x (debajo del promedio)"
            }
        
        # Regla 3: RSI en zona óptima (entre 50 y 70)
        rsi_min = self.rules["rsi_min"]
        rsi_max = self.rules["rsi_max"]
        if rsi_min <= indicators.rsi <= rsi_max:
            points = self.rules["rsi_optimal_points"]
            score += points
            breakdown["rsi"] = {
                "points": points,
                "reason": f"RSI {indicators.rsi:.1f} en zona óptima ({rsi_min}-{rsi_max})"
            }
        else:
            if indicators.rsi < rsi_min:
                reason = f"RSI {indicators.rsi:.1f} debajo de {rsi_min} (sobreventa)"
            else:
                reason = f"RSI {indicators.rsi:.1f} encima de {rsi_max} (sobrecompra)"
            breakdown["rsi"] = {"points": 0, "reason": reason}
        
        # Regla 4: Precio por encima de SMA 20
        if indicators.above_sma:
            points = self.rules["above_sma_points"]
            score += points
            breakdown["sma"] = {
                "points": points,
                "reason": f"Precio ${indicators.current_price:.2f} > SMA20 ${indicators.sma_20:.2f}"
            }
        else:
            breakdown["sma"] = {
                "points": 0,
                "reason": f"Precio ${indicators.current_price:.2f} < SMA20 ${indicators.sma_20:.2f}"
            }
        
        # Regla 5: Tendencia alcista
        if indicators.trend == "bullish":
            points = self.rules["bullish_trend_points"]
            score += points
            breakdown["trend"] = {
                "points": points,
                "reason": "Tendencia alcista en últimos 5 días"
            }
        else:
            breakdown["trend"] = {
                "points": 0,
                "reason": f"Tendencia {indicators.trend}"
            }
        
        return {
            "total_score": min(score, 10),  # Cap en 10
            "breakdown": breakdown
        }
    
    def create_cedear_score(
        self, 
        indicators: StockIndicators,
        include_breakdown: bool = True,
        ars_data: Dict = None
    ) -> CEDEARScore:
        """
        Crea el objeto CEDEARScore completo para una acción.
        
        Args:
            indicators: Indicadores técnicos
            include_breakdown: Si incluir el desglose del puntaje
            ars_data: Datos de precio en ARS {"price_ars": float, "daily_change_pct_ars": float}
            
        Returns:
            CEDEARScore con toda la información
        """
        ticker = indicators.ticker
        scoring_result = self.calculate_score(indicators)
        
        # Obtener info del CEDEAR
        cedear_info = self.universe.get(ticker, {
            "company": ticker,
            "ratio": 1
        })
        
        return CEDEARScore(
            cedear=ticker,
            company=cedear_info["company"],
            score=scoring_result["total_score"],
            daily_change_pct=indicators.daily_change_pct,
            volume_ratio=indicators.volume_ratio,
            rsi=indicators.rsi,
            trend=indicators.trend,
            current_price=indicators.current_price,
            price_ars=ars_data.get("price_ars") if ars_data else None,
            daily_change_pct_ars=ars_data.get("daily_change_pct_ars") if ars_data else None,
            score_breakdown=scoring_result["breakdown"] if include_breakdown else None
        )
    
    def rank_cedears(
        self, 
        indicators_dict: Dict[str, StockIndicators],
        include_breakdown: bool = False,
        ars_prices: Dict = None
    ) -> List[CEDEARScore]:
        """
        Rankea todos los CEDEARs por score técnico.
        
        Args:
            indicators_dict: Diccionario {ticker: StockIndicators}
            include_breakdown: Si incluir el desglose del puntaje
            ars_prices: Diccionario {ticker: {"price_ars": float, "daily_change_pct_ars": float}}
            
        Returns:
            Lista de CEDEARScore ordenada de mayor a menor score
        """
        scored_cedears = []
        
        for ticker, indicators in indicators_dict.items():
            # Solo incluir tickers que están en el universo de CEDEARs
            if ticker in self.universe:
                ars_data = ars_prices.get(ticker) if ars_prices else None
                cedear_score = self.create_cedear_score(
                    indicators, 
                    include_breakdown=include_breakdown,
                    ars_data=ars_data
                )
                scored_cedears.append(cedear_score)
            else:
                logger.warning(f"{ticker} no está en el universo de CEDEARs")
        
        # Ordenar por score descendente, luego por variación diaria
        scored_cedears.sort(
            key=lambda x: (x.score, x.daily_change_pct), 
            reverse=True
        )
        
        logger.info(f"Rankeados {len(scored_cedears)} CEDEARs")
        return scored_cedears
    
    def get_top_n(
        self, 
        indicators_dict: Dict[str, StockIndicators],
        n: int = 5,
        include_breakdown: bool = True,
        ars_prices: Dict = None
    ) -> List[CEDEARScore]:
        """
        Obtiene los top N CEDEARs por score técnico.
        
        Args:
            indicators_dict: Diccionario {ticker: StockIndicators}
            n: Número de CEDEARs a retornar
            include_breakdown: Si incluir el desglose del puntaje
            ars_prices: Diccionario {ticker: {"price_ars": float, "daily_change_pct_ars": float}}
            
        Returns:
            Lista de los top N CEDEARScore
        """
        all_ranked = self.rank_cedears(indicators_dict, include_breakdown, ars_prices)
        return all_ranked[:n]


# Instancia global del servicio
scoring_service = ScoringService()
