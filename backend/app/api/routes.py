"""
Endpoints de la API del CEDEAR Screener.
"""

from fastapi import APIRouter, HTTPException, Query
from datetime import date
from typing import Literal
import logging

from ..models import Top5Response, HealthResponse, AllCEDEARSResponse
from ..config import settings, CEDEAR_UNIVERSE
from ..services.market_data import market_data_service
from ..services.technical_analysis import technical_analysis_service
from ..services.scoring import scoring_service
from ..services.fundamental_data import fundamental_data_service
from ..services.value_scoring import value_scoring_service
from ..services.defensive_scoring import defensive_scoring_service

logger = logging.getLogger(__name__)
router = APIRouter()

DISCLAIMER = (
    "Este análisis es exclusivamente informativo y educativo. "
    "No constituye asesoramiento financiero ni recomendación de inversión. "
    "Los indicadores técnicos mostrados reflejan el comportamiento pasado "
    "y no garantizan resultados futuros."
)


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Verifica el estado del servicio.
    """
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION
    )


@router.get("/top5-cedears", response_model=Top5Response)
async def get_top5_cedears(
    include_breakdown: bool = Query(
        True, 
        description="Incluir desglose del puntaje"
    ),
    strategy: Literal["momentum", "value", "defensive"] = Query(
        "momentum",
        description="Estrategia de análisis: momentum (técnico), value (fundamentales) o defensive (baja volatilidad)"
    )
):
    """
    Obtiene el Top 6 de CEDEARs según la estrategia seleccionada.
    
    **Estrategias disponibles:**
    
    - **momentum**: Análisis técnico (variación diaria, volumen, RSI, SMA, tendencia)
    - **value**: Análisis fundamental (P/E, P/B, dividendos, ROE, deuda)
    - **defensive**: Acciones estables (beta bajo, volatilidad baja, sectores defensivos)
    
    **Nota**: Este análisis es informativo y no constituye 
    recomendación de inversión.
    """
    try:
        tickers = list(CEDEAR_UNIVERSE.keys())
        
        # Obtener precios en ARS y USD de CEDEARs
        logger.info("Obteniendo precios en ARS y USD...")
        ars_prices = market_data_service.get_cedear_prices_ars(tickers)
        usd_prices = market_data_service.get_cedear_prices_usd(tickers)
        
        if strategy == "momentum":
            # === ESTRATEGIA MOMENTUM (técnica) ===
            logger.info("Ejecutando estrategia MOMENTUM...")
            
            # 1. Obtener datos de mercado
            stocks_data = market_data_service.get_all_stocks_data(tickers)
            
            if not stocks_data:
                raise HTTPException(
                    status_code=503,
                    detail="No se pudieron obtener datos de mercado"
                )
            
            # 2. Calcular indicadores técnicos
            indicators = technical_analysis_service.analyze_multiple_stocks(stocks_data)
            
            if not indicators:
                raise HTTPException(
                    status_code=503,
                    detail="Error calculando indicadores técnicos"
                )
            
            # 3. Obtener Top 6
            top5 = scoring_service.get_top_n(
                indicators, 
                n=6, 
                include_breakdown=include_breakdown,
                ars_prices=ars_prices,
                usd_prices=usd_prices
            )
        
        elif strategy == "value":
            # === ESTRATEGIA VALUE (fundamental) ===
            logger.info("Ejecutando estrategia VALUE...")
            
            # 1. Obtener datos fundamentales
            fundamentals = fundamental_data_service.get_all_fundamentals(tickers)
            
            if not fundamentals:
                raise HTTPException(
                    status_code=503,
                    detail="No se pudieron obtener datos fundamentales"
                )
            
            # 2. Obtener precios actuales para mostrar
            stocks_data = market_data_service.get_all_stocks_data(tickers)
            prices_dict = {}
            for ticker, data in stocks_data.items():
                if not data.empty:
                    prices_dict[ticker] = float(data['Close'].iloc[-1])
            
            # 3. Obtener Top 6 por Value
            top5 = value_scoring_service.get_top_n(
                fundamentals,
                prices_dict,
                n=6, 
                include_breakdown=include_breakdown,
                ars_prices=ars_prices,
                usd_prices=usd_prices
            )
        
        elif strategy == "defensive":
            # === ESTRATEGIA DEFENSIVE (baja volatilidad) ===
            logger.info("Ejecutando estrategia DEFENSIVE...")
            
            # 1. Obtener datos fundamentales (incluye beta y sector)
            fundamentals = fundamental_data_service.get_all_fundamentals(tickers)
            
            if not fundamentals:
                raise HTTPException(
                    status_code=503,
                    detail="No se pudieron obtener datos fundamentales"
                )
            
            # 2. Obtener datos históricos para calcular volatilidad
            stocks_data = market_data_service.get_all_stocks_data(tickers)
            prices_dict = {}
            for ticker, data in stocks_data.items():
                if not data.empty:
                    prices_dict[ticker] = float(data['Close'].iloc[-1])
            
            # 3. Obtener Top 6 por Defensive
            top5 = defensive_scoring_service.get_top_n(
                fundamentals,
                stocks_data,
                prices_dict,
                n=6, 
                include_breakdown=include_breakdown,
                ars_prices=ars_prices,
                usd_prices=usd_prices
            )
        
        return Top5Response(
            date=date.today().isoformat(),
            disclaimer=DISCLAIMER,
            top5=top5
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en /top5-cedears: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get("/cedears", response_model=AllCEDEARSResponse)
async def get_all_cedears(
    include_breakdown: bool = Query(
        False, 
        description="Incluir desglose del puntaje"
    )
):
    """
    Obtiene el análisis técnico de todos los CEDEARs del universo.
    
    Retorna la lista completa ordenada por score técnico de mayor a menor.
    """
    try:
        # Obtener datos
        tickers = list(CEDEAR_UNIVERSE.keys())
        stocks_data = market_data_service.get_all_stocks_data(tickers)
        
        if not stocks_data:
            raise HTTPException(
                status_code=503,
                detail="No se pudieron obtener datos de mercado"
            )
        
        # Calcular indicadores
        indicators = technical_analysis_service.analyze_multiple_stocks(stocks_data)
        
        # Obtener precios en ARS y USD
        ars_prices = market_data_service.get_cedear_prices_ars(tickers)
        usd_prices = market_data_service.get_cedear_prices_usd(tickers)
        
        # Rankear todos
        all_cedears = scoring_service.rank_cedears(
            indicators, 
            include_breakdown=include_breakdown,
            ars_prices=ars_prices,
            usd_prices=usd_prices
        )
        
        return AllCEDEARSResponse(
            date=date.today().isoformat(),
            disclaimer=DISCLAIMER,
            total=len(all_cedears),
            cedears=all_cedears
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en /cedears: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get("/cedears/{ticker}")
async def get_cedear_detail(ticker: str):
    """
    Obtiene el análisis técnico detallado de un CEDEAR específico.
    
    Args:
        ticker: Símbolo de la acción subyacente (ej: AAPL)
    """
    ticker = ticker.upper()
    
    if ticker not in CEDEAR_UNIVERSE:
        raise HTTPException(
            status_code=404,
            detail=f"CEDEAR {ticker} no encontrado en el universo"
        )
    
    try:
        # Obtener datos
        stocks_data = market_data_service.get_all_stocks_data([ticker])
        
        if ticker not in stocks_data:
            raise HTTPException(
                status_code=503,
                detail=f"No se pudieron obtener datos para {ticker}"
            )
        
        # Calcular indicadores
        indicators = technical_analysis_service.calculate_all_indicators(
            ticker, 
            stocks_data[ticker]
        )
        
        if not indicators:
            raise HTTPException(
                status_code=503,
                detail=f"Error calculando indicadores para {ticker}"
            )
        
        # Crear score
        cedear_score = scoring_service.create_cedear_score(
            indicators, 
            include_breakdown=True
        )
        
        return {
            "date": date.today().isoformat(),
            "disclaimer": DISCLAIMER,
            "cedear": cedear_score.model_dump()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en /cedears/{ticker}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get("/universe")
async def get_universe():
    """
    Retorna el universo de CEDEARs disponibles para análisis.
    """
    return {
        "total": len(CEDEAR_UNIVERSE),
        "cedears": [
            {
                "ticker": ticker,
                "company": info["company"],
                "ratio": info["ratio"]
            }
            for ticker, info in CEDEAR_UNIVERSE.items()
        ]
    }
