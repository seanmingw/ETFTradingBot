"""Fund API routes supporting exchange (场内) and offline (场外) funds."""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from ..services.exchange_fund_service import ExchangeFundService
from ..services.offline_fund_service import OfflineFundService
from ..models.fund import FundWithMetrics, FundScreenerRequest

router = APIRouter(prefix="/api/funds", tags=["Funds"])

exchange_fund_service = ExchangeFundService()
offline_fund_service = OfflineFundService()

@router.get("/list", response_model=List[FundWithMetrics])
async def get_funds(
    fund_type: Optional[str] = Query(None, description="Filter by fund type: 'exchange' or 'offline'"),
    region: Optional[str] = Query(None, description="Filter by region"),
    category: Optional[str] = Query(None, description="Filter by category")
):
    """Get all funds with optional filters."""
    try:
        funds = []

        if fund_type is None or fund_type == 'exchange':
            exchange_funds = exchange_fund_service.get_exchange_funds_by_region(region)
            funds.extend(exchange_funds)

        if fund_type is None or fund_type == 'offline':
            offline_funds = offline_fund_service.get_offline_funds_by_category(category)
            funds.extend(offline_funds)

        if region:
            funds = [f for f in funds if f.get('region') == region]

        return funds
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/exchange", response_model=List[FundWithMetrics])
async def get_exchange_funds(region: Optional[str] = None):
    """Get exchange traded funds (场内基金)."""
    try:
        return exchange_fund_service.get_exchange_funds_by_region(region)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/offline", response_model=List[FundWithMetrics])
async def get_offline_funds(category: Optional[str] = None):
    """Get offline funds (场外基金)."""
    try:
        return offline_fund_service.get_offline_funds_by_category(category)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{symbol}", response_model=FundWithMetrics)
async def get_fund(symbol: str):
    """Get fund details by symbol."""
    try:
        fund = exchange_fund_service.get_fund_by_symbol(symbol)
        if not fund:
            fund = offline_fund_service.get_fund_by_symbol(symbol)

        if not fund:
            raise HTTPException(status_code=404, detail=f"Fund {symbol} not found")

        return fund
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search/", response_model=List[FundWithMetrics])
async def search_funds(
    q: str = Query(..., min_length=1, description="Search query"),
    fund_type: Optional[str] = None
):
    """Search funds by name or symbol."""
    try:
        results = []
        query_lower = q.lower()

        if fund_type is None or fund_type == 'exchange':
            exchange_funds = exchange_fund_service.get_exchange_funds_by_region()
            results.extend([f for f in exchange_funds
                          if query_lower in f['symbol'].lower() or query_lower in f['name'].lower()])

        if fund_type is None or fund_type == 'offline':
            offline_funds = offline_fund_service.get_all_offline_funds()
            results.extend([f for f in offline_funds
                          if query_lower in f['symbol'].lower() or query_lower in f['name'].lower()])

        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/categories/exchange")
async def get_exchange_regions():
    """Get available exchange regions."""
    return {
        'regions': list(ExchangeFundService.EXCHANGE_FUNDS.keys())
    }

@router.get("/categories/offline")
async def get_offline_categories():
    """Get available offline fund categories."""
    return {
        'categories': {
            'Equity': '股票型',
            'Bond': '债券型',
            'Index': '指数型',
            'International': 'QDII型'
        }
    }
