"""ETF API routes."""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from ..services.etf_service import ETFService
from ..models.etf import ETFWithMetrics, ETFScreenerRequest

router = APIRouter(prefix="/api/etf", tags=["ETF"])

etf_service = ETFService()

@router.get("/list", response_model=List[ETFWithMetrics])
async def get_etf_list(region: Optional[str] = None):
    """Get list of all available ETFs."""
    try:
        return etf_service.get_all_etfs(region)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{symbol}", response_model=ETFWithMetrics)
async def get_etf(symbol: str):
    """Get detailed information for a specific ETF."""
    try:
        etf = etf_service.get_etf_by_symbol(symbol.upper())
        if not etf:
            raise HTTPException(status_code=404, detail=f"ETF {symbol} not found")
        return etf
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search/", response_model=List[ETFWithMetrics])
async def search_etfs(q: str = Query(..., min_length=1), region: Optional[str] = None):
    """Search ETFs by name or symbol."""
    try:
        return etf_service.search_etfs(q, region)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/screen", response_model=List[ETFWithMetrics])
async def screen_etfs(criteria: ETFScreenerRequest):
    """Screen ETFs based on given criteria."""
    try:
        return etf_service.screen_etfs(criteria)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/compare/")
async def compare_etfs(symbols: str = Query(..., description="Comma-separated list of symbols")):
    """Compare multiple ETFs."""
    try:
        symbol_list = [s.strip().upper() for s in symbols.split(',')]
        return etf_service.get_etf_comparison(symbol_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{symbol}/indicators")
async def get_technical_indicators(symbol: str, period: str = "1y"):
    """Get technical indicators for an ETF."""
    try:
        indicators = etf_service.get_technical_indicators(symbol.upper(), period)
        if not indicators:
            raise HTTPException(status_code=404, detail=f"Unable to fetch indicators for {symbol}")
        return indicators
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
