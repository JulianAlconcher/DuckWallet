"""
Servicio de scoring para estrategia Global.
Muestra CEDEARs que aparecen en más de una estrategia (momentum, value, defensive).
"""

from typing import Dict, List, Optional, Set
import logging

from ..config import CEDEAR_UNIVERSE
from ..models import CEDEARScore

logger = logging.getLogger(__name__)


class GlobalScoringService:
    """
    Servicio para identificar CEDEARs que destacan en múltiples estrategias.
    Un CEDEAR "global" es aquel que aparece en el top de más de una estrategia.
    """
    
    def __init__(self):
        self.universe = CEDEAR_UNIVERSE
    
    def get_global_cedears(
        self,
        momentum_results: List[CEDEARScore],
        value_results: List[CEDEARScore],
        defensive_results: List[CEDEARScore],
        top_n_per_strategy: int = 10,
        max_results: int = 6
    ) -> List[CEDEARScore]:
        """
        Encuentra CEDEARs que aparecen en el top de múltiples estrategias.
        Si no hay suficientes, combina los mejores de cada estrategia.
        
        Args:
            momentum_results: Top CEDEARs por momentum
            value_results: Top CEDEARs por value
            defensive_results: Top CEDEARs por defensive
            top_n_per_strategy: Cuántos considerar del top de cada estrategia
            max_results: Máximo de resultados a devolver
            
        Returns:
            Lista de CEDEARScore de los que aparecen en múltiples estrategias
        """
        # Obtener los tickers del top de cada estrategia
        momentum_tickers = set(r.cedear for r in momentum_results[:top_n_per_strategy])
        value_tickers = set(r.cedear for r in value_results[:top_n_per_strategy])
        defensive_tickers = set(r.cedear for r in defensive_results[:top_n_per_strategy])
        
        # Contar en cuántas estrategias aparece cada ticker
        ticker_counts: Dict[str, int] = {}
        ticker_strategies: Dict[str, List[str]] = {}
        
        for ticker in momentum_tickers:
            ticker_counts[ticker] = ticker_counts.get(ticker, 0) + 1
            ticker_strategies.setdefault(ticker, []).append("Momentum")
        
        for ticker in value_tickers:
            ticker_counts[ticker] = ticker_counts.get(ticker, 0) + 1
            ticker_strategies.setdefault(ticker, []).append("Value")
        
        for ticker in defensive_tickers:
            ticker_counts[ticker] = ticker_counts.get(ticker, 0) + 1
            ticker_strategies.setdefault(ticker, []).append("Defensivo")
        
        # Filtrar los que aparecen en más de una estrategia
        global_tickers = {t for t, count in ticker_counts.items() if count >= 2}
        
        # Si no hay suficientes coincidencias, combinar los mejores de cada estrategia
        if len(global_tickers) < 3:
            logger.info(f"Solo {len(global_tickers)} CEDEARs multi-estrategia, combinando mejores de cada una")
            # Tomar el #1 de cada estrategia (sin repetir)
            combined = []
            seen = set()
            for result_list in [momentum_results, value_results, defensive_results]:
                if result_list:
                    for r in result_list:
                        if r.cedear not in seen:
                            combined.append(r)
                            seen.add(r.cedear)
                            break
            # Si aún no tenemos 3, agregar más de momentum
            for r in momentum_results:
                if r.cedear not in seen and len(combined) < max_results:
                    combined.append(r)
                    seen.add(r.cedear)
            return combined[:max_results]
        
        logger.info(f"CEDEARs globales encontrados: {global_tickers}")
        
        # Crear resultados combinados
        # Usamos los datos de momentum como base, pero con score combinado
        results = []
        
        # Crear un mapa de resultados por ticker para cada estrategia
        momentum_map = {r.cedear: r for r in momentum_results}
        value_map = {r.cedear: r for r in value_results}
        defensive_map = {r.cedear: r for r in defensive_results}
        
        for ticker in global_tickers:
            # Calcular score promedio de las estrategias donde aparece
            scores = []
            strategies_info = {}
            
            if ticker in momentum_map:
                scores.append(momentum_map[ticker].score)
                strategies_info["momentum"] = {
                    "points": momentum_map[ticker].score,
                    "reason": f"Top en Momentum (score {momentum_map[ticker].score})"
                }
            
            if ticker in value_map:
                scores.append(value_map[ticker].score)
                strategies_info["value"] = {
                    "points": value_map[ticker].score,
                    "reason": f"Top en Value (score {value_map[ticker].score})"
                }
            
            if ticker in defensive_map:
                scores.append(defensive_map[ticker].score)
                strategies_info["defensive"] = {
                    "points": defensive_map[ticker].score,
                    "reason": f"Top en Defensivo (score {defensive_map[ticker].score})"
                }
            
            avg_score = round(sum(scores) / len(scores))
            num_strategies = len(scores)
            
            # Agregar bonus por aparecer en múltiples estrategias
            strategies_info["multi_strategy_bonus"] = {
                "points": num_strategies,
                "reason": f"Aparece en {num_strategies} estrategias: {', '.join(ticker_strategies[ticker])}"
            }
            
            # Usar datos base del momentum si está disponible, sino value, sino defensive
            base_data = momentum_map.get(ticker) or value_map.get(ticker) or defensive_map.get(ticker)
            
            if base_data:
                result = CEDEARScore(
                    cedear=ticker,
                    company=base_data.company,
                    score=min(10, avg_score + num_strategies - 1),  # Bonus por multi-estrategia
                    daily_change_pct=base_data.daily_change_pct,
                    volume_ratio=float(num_strategies),  # Usamos para mostrar # de estrategias
                    rsi=avg_score,  # Score promedio
                    trend="bullish" if avg_score >= 7 else "neutral",
                    current_price=base_data.current_price,
                    price_ars=base_data.price_ars,
                    daily_change_pct_ars=base_data.daily_change_pct_ars,
                    price_usd=base_data.price_usd,
                    daily_change_pct_usd=base_data.daily_change_pct_usd,
                    score_breakdown=strategies_info
                )
                results.append(result)
        
        # Ordenar por score descendente
        results.sort(key=lambda x: x.score, reverse=True)
        
        return results[:max_results]


# Instancia global del servicio
global_scoring_service = GlobalScoringService()
