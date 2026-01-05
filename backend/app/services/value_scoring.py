"""
Servicio de scoring para estrategia Value.
Busca acciones "baratas" con buenos fundamentales.
"""

from typing import Dict, List, Optional
import logging

from ..config import CEDEAR_UNIVERSE
from ..models import CEDEARScore

logger = logging.getLogger(__name__)


# Reglas de scoring para estrategia Value
VALUE_SCORING_RULES = {
    # P/E Ratio - bajo es mejor
    "pe_low_threshold": 15,       # P/E < 15 es excelente
    "pe_medium_threshold": 25,    # P/E < 25 es aceptable
    "pe_low_points": 3,
    "pe_medium_points": 1,
    
    # Price to Book - bajo es mejor
    "pb_low_threshold": 3,        # P/B < 3 es bueno
    "pb_points": 2,
    
    # Dividend Yield - alto es mejor
    "dividend_threshold": 0.02,   # > 2% dividendo
    "dividend_points": 2,
    
    # ROE - alto es mejor (calidad)
    "roe_threshold": 0.15,        # > 15% ROE
    "roe_points": 2,
    
    # Debt to Equity - bajo es mejor
    "debt_threshold": 100,        # D/E < 100%
    "debt_points": 1,
}


class ValueScoringService:
    """
    Servicio para calcular el score Value de cada CEDEAR.
    Busca acciones baratas con buenos fundamentales.
    """
    
    def __init__(self):
        self.rules = VALUE_SCORING_RULES
        self.universe = CEDEAR_UNIVERSE
    
    def calculate_score(self, fundamentals: Dict) -> Dict:
        """
        Calcula el score Value para una acción basado en fundamentales.
        
        Sistema de puntuación:
        - +3 puntos: P/E < 15 (muy barato)
        - +1 punto: P/E entre 15 y 25
        - +2 puntos: Price/Book < 3
        - +2 puntos: Dividend Yield > 2%
        - +2 puntos: ROE > 15%
        - +1 punto: Debt/Equity < 100%
        
        Máximo: 10 puntos
        
        Args:
            fundamentals: Datos fundamentales de la acción
            
        Returns:
            Diccionario con score total y desglose
        """
        score = 0
        breakdown = {}
        
        # Regla 1: P/E Ratio bajo
        pe = fundamentals.get("pe_ratio")
        if pe is not None and pe > 0:
            if pe < self.rules["pe_low_threshold"]:
                points = self.rules["pe_low_points"]
                score += points
                breakdown["pe_ratio"] = {
                    "points": points,
                    "reason": f"P/E {pe:.1f} < {self.rules['pe_low_threshold']} (muy barato)"
                }
            elif pe < self.rules["pe_medium_threshold"]:
                points = self.rules["pe_medium_points"]
                score += points
                breakdown["pe_ratio"] = {
                    "points": points,
                    "reason": f"P/E {pe:.1f} < {self.rules['pe_medium_threshold']} (aceptable)"
                }
            else:
                breakdown["pe_ratio"] = {
                    "points": 0,
                    "reason": f"P/E {pe:.1f} >= {self.rules['pe_medium_threshold']} (caro)"
                }
        else:
            breakdown["pe_ratio"] = {
                "points": 0,
                "reason": "P/E no disponible o negativo"
            }
        
        # Regla 2: Price to Book bajo
        pb = fundamentals.get("price_to_book")
        if pb is not None and pb > 0:
            if pb < self.rules["pb_low_threshold"]:
                points = self.rules["pb_points"]
                score += points
                breakdown["price_to_book"] = {
                    "points": points,
                    "reason": f"P/B {pb:.1f} < {self.rules['pb_low_threshold']} (barato vs activos)"
                }
            else:
                breakdown["price_to_book"] = {
                    "points": 0,
                    "reason": f"P/B {pb:.1f} >= {self.rules['pb_low_threshold']}"
                }
        else:
            breakdown["price_to_book"] = {
                "points": 0,
                "reason": "P/B no disponible"
            }
        
        # Regla 3: Dividend Yield alto
        div_yield = fundamentals.get("dividend_yield")
        if div_yield is not None and div_yield > 0:
            if div_yield >= self.rules["dividend_threshold"]:
                points = self.rules["dividend_points"]
                score += points
                breakdown["dividend"] = {
                    "points": points,
                    "reason": f"Dividendo {div_yield*100:.1f}% >= {self.rules['dividend_threshold']*100}%"
                }
            else:
                breakdown["dividend"] = {
                    "points": 0,
                    "reason": f"Dividendo {div_yield*100:.1f}% < {self.rules['dividend_threshold']*100}%"
                }
        else:
            breakdown["dividend"] = {
                "points": 0,
                "reason": "No paga dividendo"
            }
        
        # Regla 4: ROE alto (calidad)
        roe = fundamentals.get("roe")
        if roe is not None:
            if roe >= self.rules["roe_threshold"]:
                points = self.rules["roe_points"]
                score += points
                breakdown["roe"] = {
                    "points": points,
                    "reason": f"ROE {roe*100:.1f}% >= {self.rules['roe_threshold']*100}% (rentable)"
                }
            else:
                breakdown["roe"] = {
                    "points": 0,
                    "reason": f"ROE {roe*100:.1f}% < {self.rules['roe_threshold']*100}%"
                }
        else:
            breakdown["roe"] = {
                "points": 0,
                "reason": "ROE no disponible"
            }
        
        # Regla 5: Deuda baja
        debt = fundamentals.get("debt_to_equity")
        if debt is not None:
            if debt < self.rules["debt_threshold"]:
                points = self.rules["debt_points"]
                score += points
                breakdown["debt"] = {
                    "points": points,
                    "reason": f"Deuda/Patrimonio {debt:.0f}% < {self.rules['debt_threshold']}%"
                }
            else:
                breakdown["debt"] = {
                    "points": 0,
                    "reason": f"Deuda/Patrimonio {debt:.0f}% >= {self.rules['debt_threshold']}% (endeudada)"
                }
        else:
            breakdown["debt"] = {
                "points": 0,
                "reason": "Datos de deuda no disponibles"
            }
        
        return {
            "total_score": min(score, 10),
            "breakdown": breakdown
        }
    
    def create_cedear_score(
        self, 
        ticker: str,
        fundamentals: Dict,
        current_price: float,
        include_breakdown: bool = True,
        ars_data: Optional[Dict] = None,
        usd_data: Optional[Dict] = None
    ) -> CEDEARScore:
        """
        Crea el objeto CEDEARScore para estrategia Value.
        """
        scoring_result = self.calculate_score(fundamentals)
        
        cedear_info = self.universe.get(ticker, {
            "company": ticker,
            "ratio": 1
        })
        
        # Para Value, mostramos el P/E en lugar de RSI
        pe = fundamentals.get("pe_ratio") or 0
        div_yield = fundamentals.get("dividend_yield") or 0
        
        return CEDEARScore(
            cedear=ticker,
            company=cedear_info["company"],
            score=scoring_result["total_score"],
            daily_change_pct=div_yield * 100,  # Usamos este campo para mostrar dividend yield
            volume_ratio=pe / 10 if pe else 0,  # Normalizamos P/E para mostrar
            rsi=pe,  # Mostramos P/E en el campo RSI
            trend="neutral",  # Value no mira tendencia
            current_price=current_price,
            price_ars=ars_data.get("price_ars") if ars_data else None,
            daily_change_pct_ars=ars_data.get("daily_change_pct_ars") if ars_data else None,
            price_usd=usd_data.get("price_usd") if usd_data else None,
            daily_change_pct_usd=usd_data.get("daily_change_pct_usd") if usd_data else None,
            score_breakdown=scoring_result["breakdown"] if include_breakdown else None
        )
    
    def rank_cedears(
        self, 
        fundamentals_dict: Dict[str, Dict],
        prices_dict: Dict[str, float],
        include_breakdown: bool = False,
        ars_prices: Optional[Dict] = None,
        usd_prices: Optional[Dict] = None
    ) -> List[CEDEARScore]:
        """
        Rankea todos los CEDEARs por score Value.
        """
        scored_cedears = []
        
        for ticker, fundamentals in fundamentals_dict.items():
            if ticker in self.universe:
                ars_data = ars_prices.get(ticker) if ars_prices else None
                usd_data = usd_prices.get(ticker) if usd_prices else None
                price = prices_dict.get(ticker, 0)
                
                cedear_score = self.create_cedear_score(
                    ticker=ticker,
                    fundamentals=fundamentals,
                    current_price=price,
                    include_breakdown=include_breakdown,
                    ars_data=ars_data,
                    usd_data=usd_data
                )
                scored_cedears.append(cedear_score)
        
        # Ordenar por score descendente
        scored_cedears.sort(key=lambda x: x.score, reverse=True)
        
        logger.info(f"Rankeados {len(scored_cedears)} CEDEARs por Value")
        return scored_cedears
    
    def get_top_n(
        self, 
        fundamentals_dict: Dict[str, Dict],
        prices_dict: Dict[str, float],
        n: int = 6,
        include_breakdown: bool = True,
        ars_prices: Optional[Dict] = None,
        usd_prices: Optional[Dict] = None
    ) -> List[CEDEARScore]:
        """
        Obtiene los top N CEDEARs por score Value.
        """
        all_ranked = self.rank_cedears(
            fundamentals_dict, 
            prices_dict, 
            include_breakdown, 
            ars_prices,
            usd_prices
        )
        return all_ranked[:n]


# Instancia global del servicio
value_scoring_service = ValueScoringService()
