"""
Servicio de scoring para estrategia Defensivo.
Busca acciones estables con baja volatilidad.
"""

from typing import Dict, List, Optional
import logging
import numpy as np

from ..config import CEDEAR_UNIVERSE
from ..models import CEDEARScore

logger = logging.getLogger(__name__)


# Sectores considerados defensivos
DEFENSIVE_SECTORS = [
    "Consumer Defensive",
    "Healthcare",
    "Utilities",
    "Consumer Staples",
    "Health Care",
]

# Reglas de scoring para estrategia Defensivo
DEFENSIVE_SCORING_RULES = {
    # Beta bajo - menor volatilidad que el mercado
    "beta_low_threshold": 0.8,      # Beta < 0.8 es muy defensivo
    "beta_medium_threshold": 1.0,   # Beta < 1.0 es aceptable
    "beta_low_points": 3,
    "beta_medium_points": 1,
    
    # Volatilidad baja (desviación estándar de retornos)
    "volatility_low_threshold": 0.02,   # < 2% volatilidad diaria
    "volatility_medium_threshold": 0.03, # < 3% volatilidad diaria
    "volatility_low_points": 2,
    "volatility_medium_points": 1,
    
    # Dividend Yield - ingresos estables
    "dividend_threshold": 0.015,    # > 1.5% dividendo
    "dividend_points": 2,
    
    # Sector defensivo
    "defensive_sector_points": 2,
    
    # Deuda baja - estabilidad financiera
    "debt_low_threshold": 50,       # D/E < 50%
    "debt_medium_threshold": 100,   # D/E < 100%
    "debt_low_points": 2,
    "debt_medium_points": 1,
}


class DefensiveScoringService:
    """
    Servicio para calcular el score Defensivo de cada CEDEAR.
    Busca acciones estables con baja volatilidad.
    """
    
    def __init__(self):
        self.rules = DEFENSIVE_SCORING_RULES
        self.universe = CEDEAR_UNIVERSE
    
    def calculate_volatility(self, historical_data) -> Optional[float]:
        """
        Calcula la volatilidad histórica (desviación estándar de retornos diarios).
        
        Args:
            historical_data: DataFrame con datos históricos
            
        Returns:
            Volatilidad como decimal (ej: 0.02 = 2%)
        """
        try:
            if historical_data is None or historical_data.empty:
                return None
            
            # Calcular retornos diarios
            returns = historical_data['Close'].pct_change().dropna()
            
            if len(returns) < 20:
                return None
            
            # Desviación estándar de los retornos
            volatility = returns.std()
            return float(volatility)
        except Exception as e:
            logger.error(f"Error calculando volatilidad: {e}")
            return None
    
    def calculate_score(self, fundamentals: Dict, volatility: Optional[float] = None) -> Dict:
        """
        Calcula el score Defensivo para una acción.
        
        Sistema de puntuación:
        - +3 puntos: Beta < 0.8 (muy estable)
        - +1 punto: Beta entre 0.8 y 1.0
        - +2 puntos: Volatilidad < 2%
        - +1 punto: Volatilidad entre 2% y 3%
        - +2 puntos: Dividend Yield > 1.5%
        - +2 puntos: Sector defensivo
        - +2 puntos: Debt/Equity < 50%
        - +1 punto: Debt/Equity entre 50% y 100%
        
        Máximo: ~11 puntos (normalizado a 10)
        
        Args:
            fundamentals: Datos fundamentales de la acción
            volatility: Volatilidad calculada
            
        Returns:
            Diccionario con score total y desglose
        """
        score = 0
        breakdown = {}
        
        # Regla 1: Beta bajo
        beta = fundamentals.get("beta")
        if beta is not None and beta > 0:
            if beta < self.rules["beta_low_threshold"]:
                points = self.rules["beta_low_points"]
                score += points
                breakdown["beta"] = {
                    "points": points,
                    "reason": f"Beta {beta:.2f} < {self.rules['beta_low_threshold']} (muy estable)"
                }
            elif beta < self.rules["beta_medium_threshold"]:
                points = self.rules["beta_medium_points"]
                score += points
                breakdown["beta"] = {
                    "points": points,
                    "reason": f"Beta {beta:.2f} < {self.rules['beta_medium_threshold']} (estable)"
                }
            else:
                breakdown["beta"] = {
                    "points": 0,
                    "reason": f"Beta {beta:.2f} >= {self.rules['beta_medium_threshold']} (volátil)"
                }
        else:
            breakdown["beta"] = {
                "points": 0,
                "reason": "Beta no disponible"
            }
        
        # Regla 2: Volatilidad baja
        if volatility is not None:
            vol_pct = volatility * 100
            if volatility < self.rules["volatility_low_threshold"]:
                points = self.rules["volatility_low_points"]
                score += points
                breakdown["volatility"] = {
                    "points": points,
                    "reason": f"Volatilidad {vol_pct:.1f}% < {self.rules['volatility_low_threshold']*100}% (muy baja)"
                }
            elif volatility < self.rules["volatility_medium_threshold"]:
                points = self.rules["volatility_medium_points"]
                score += points
                breakdown["volatility"] = {
                    "points": points,
                    "reason": f"Volatilidad {vol_pct:.1f}% < {self.rules['volatility_medium_threshold']*100}% (baja)"
                }
            else:
                breakdown["volatility"] = {
                    "points": 0,
                    "reason": f"Volatilidad {vol_pct:.1f}% >= {self.rules['volatility_medium_threshold']*100}% (alta)"
                }
        else:
            breakdown["volatility"] = {
                "points": 0,
                "reason": "Volatilidad no disponible"
            }
        
        # Regla 3: Dividendos
        dividend = fundamentals.get("dividend_yield")
        if dividend is not None and dividend > 0:
            if dividend >= self.rules["dividend_threshold"]:
                points = self.rules["dividend_points"]
                score += points
                breakdown["dividend"] = {
                    "points": points,
                    "reason": f"Dividendo {dividend*100:.1f}% >= {self.rules['dividend_threshold']*100}%"
                }
            else:
                breakdown["dividend"] = {
                    "points": 0,
                    "reason": f"Dividendo {dividend*100:.1f}% < {self.rules['dividend_threshold']*100}%"
                }
        else:
            breakdown["dividend"] = {
                "points": 0,
                "reason": "Sin dividendo"
            }
        
        # Regla 4: Sector defensivo
        sector = fundamentals.get("sector", "")
        if sector in DEFENSIVE_SECTORS:
            points = self.rules["defensive_sector_points"]
            score += points
            breakdown["sector"] = {
                "points": points,
                "reason": f"Sector defensivo: {sector}"
            }
        else:
            breakdown["sector"] = {
                "points": 0,
                "reason": f"Sector no defensivo: {sector or 'N/A'}"
            }
        
        # Regla 5: Deuda baja
        debt = fundamentals.get("debt_to_equity")
        if debt is not None:
            if debt < self.rules["debt_low_threshold"]:
                points = self.rules["debt_low_points"]
                score += points
                breakdown["debt"] = {
                    "points": points,
                    "reason": f"Deuda/Equity {debt:.0f}% < {self.rules['debt_low_threshold']}% (muy baja)"
                }
            elif debt < self.rules["debt_medium_threshold"]:
                points = self.rules["debt_medium_points"]
                score += points
                breakdown["debt"] = {
                    "points": points,
                    "reason": f"Deuda/Equity {debt:.0f}% < {self.rules['debt_medium_threshold']}% (aceptable)"
                }
            else:
                breakdown["debt"] = {
                    "points": 0,
                    "reason": f"Deuda/Equity {debt:.0f}% >= {self.rules['debt_medium_threshold']}% (alta)"
                }
        else:
            breakdown["debt"] = {
                "points": 0,
                "reason": "Deuda/Equity no disponible"
            }
        
        # Normalizar score a máximo 10
        max_possible = 11  # 3+2+2+2+2
        normalized_score = min(10, round(score * 10 / max_possible))
        
        return {
            "raw_score": score,
            "score": normalized_score,
            "breakdown": breakdown
        }
    
    def get_top_n(
        self, 
        fundamentals: Dict[str, Dict],
        stocks_data: Dict,
        prices_dict: Dict[str, float],
        n: int = 6, 
        include_breakdown: bool = True,
        ars_prices: Optional[Dict[str, Dict]] = None,
        usd_prices: Optional[Dict[str, Dict]] = None
    ) -> List[CEDEARScore]:
        """
        Obtiene los top N CEDEARs por score defensivo.
        
        Args:
            fundamentals: Diccionario con fundamentales por ticker
            stocks_data: Diccionario con datos históricos por ticker
            prices_dict: Diccionario con precios actuales
            n: Cantidad de resultados
            include_breakdown: Si incluir desglose
            ars_prices: Precios en ARS
            usd_prices: Precios en USD
            
        Returns:
            Lista de CEDEARScore ordenados por score
        """
        results = []
        
        for ticker, fund in fundamentals.items():
            # Calcular volatilidad desde datos históricos
            volatility = None
            if ticker in stocks_data and stocks_data[ticker] is not None:
                volatility = self.calculate_volatility(stocks_data[ticker])
            
            # Calcular score
            score_result = self.calculate_score(fund, volatility)
            
            # Obtener precios
            current_price = prices_dict.get(ticker, 0)
            price_ars = None
            daily_change_ars = None
            price_usd = None
            daily_change_usd = None
            
            if ars_prices and ticker in ars_prices:
                price_ars = ars_prices[ticker].get("price_ars")
                daily_change_ars = ars_prices[ticker].get("daily_change_pct_ars")
            
            if usd_prices and ticker in usd_prices:
                price_usd = usd_prices[ticker].get("price_usd")
                daily_change_usd = usd_prices[ticker].get("daily_change_pct_usd")
            
            # Crear resultado con campos mapeados para el frontend
            # Usamos campos existentes del modelo para compatibilidad
            beta = fund.get("beta", 0) or 0
            vol_pct = (volatility * 100) if volatility else 0
            
            # Obtener nombre de la empresa desde el universo
            company_info = self.universe.get(ticker, {})
            company_name = company_info.get("company", ticker) if isinstance(company_info, dict) else ticker
            
            result = CEDEARScore(
                cedear=ticker,
                company=company_name,
                score=score_result["score"],
                # Mapeamos a campos existentes del modelo
                daily_change_pct=vol_pct,  # Volatilidad %
                volume_ratio=beta,          # Beta
                rsi=fund.get("dividend_yield", 0) * 100 if fund.get("dividend_yield") else 0,  # Div yield %
                trend="neutral",  # Usamos neutral para defensivo (el modelo no acepta "stable")
                current_price=current_price,
                price_ars=price_ars,
                daily_change_pct_ars=daily_change_ars,
                price_usd=price_usd,
                daily_change_pct_usd=daily_change_usd,
                score_breakdown=score_result["breakdown"] if include_breakdown else None
            )
            results.append(result)
        
        # Ordenar por score descendente
        results.sort(key=lambda x: x.score, reverse=True)
        
        return results[:n]


# Instancia global del servicio
defensive_scoring_service = DefensiveScoringService()
