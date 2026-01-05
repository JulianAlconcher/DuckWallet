"""
Endpoints de la API del CEDEAR Screener.
"""

from fastapi import APIRouter, HTTPException, Query
from datetime import date
import logging

from ..models import Top5Response, HealthResponse, AllCEDEARSResponse
from ..config import settings, CEDEAR_UNIVERSE
from ..services.market_data import market_data_service
from ..services.technical_analysis import technical_analysis_service
from ..services.scoring import scoring_service

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
    )
):
    """
    Obtiene el Top 5 de CEDEARs con mayor fortaleza técnica.
    
    El análisis se basa en indicadores técnicos de las acciones subyacentes
    que cotizan en NASDAQ/NYSE. Los CEDEARs se ordenan según un sistema
    de scoring transparente basado en:
    
    - Variación porcentual diaria
    - Volumen relativo al promedio
    - RSI (Relative Strength Index)
    - Posición respecto a la SMA de 20 períodos
    - Tendencia reciente
    
    **Nota**: Este análisis es informativo y no constituye 
    recomendación de inversión.
    """
    try:
        # 1. Obtener datos de mercado
        logger.info("Obteniendo datos de mercado...")
        tickers = list(CEDEAR_UNIVERSE.keys())
        stocks_data = market_data_service.get_all_stocks_data(tickers)
        
        if not stocks_data:
            raise HTTPException(
                status_code=503,
                detail="No se pudieron obtener datos de mercado"
            )
        
        # 2. Calcular indicadores técnicos
        logger.info("Calculando indicadores técnicos...")
        indicators = technical_analysis_service.analyze_multiple_stocks(stocks_data)
        
        if not indicators:
            raise HTTPException(
                status_code=503,
                detail="Error calculando indicadores técnicos"
            )
        
        # 3. Obtener Top 5
        logger.info("Calculando Top 5...")
        top5 = scoring_service.get_top_n(
            indicators, 
            n=5, 
            include_breakdown=include_breakdown
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
        
        # Rankear todos
        all_cedears = scoring_service.rank_cedears(
            indicators, 
            include_breakdown=include_breakdown
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
