"""Trading API routes."""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from ..services.trading_service import TradingService
from ..services.ai_service import AIService
from ..models.trade import TradeRequest, TradeResponse, PortfolioSummary, Position, TradingSignal
import os

router = APIRouter(prefix="/api/trades", tags=["Trading"])

trading_service = TradingService(
    api_key=os.getenv('ALPACA_API_KEY'),
    api_secret=os.getenv('ALPACA_API_SECRET')
)

@router.post("/", response_model=TradeResponse)
async def execute_trade(trade_request: TradeRequest):
    """Execute a new trade."""
    try:
        return trading_service.execute_trade(trade_request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=list[TradeResponse])
async def get_trades(limit: int = Query(default=50, ge=1, le=500)):
    """Get trade history."""
    try:
        return trading_service.get_trades(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{trade_id}")
async def cancel_trade(trade_id: int):
    """Cancel a pending trade."""
    try:
        success = trading_service.cancel_trade(trade_id)
        if not success:
            raise HTTPException(status_code=404, detail="Trade not found or already executed")
        return {"message": "Trade cancelled successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/positions", response_model=list[Position])
async def get_positions():
    """Get current positions."""
    try:
        return trading_service.get_positions()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/portfolio", response_model=PortfolioSummary)
async def get_portfolio():
    """Get portfolio summary."""
    try:
        return trading_service.get_portfolio_summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/signals", response_model=list[TradingSignal])
async def generate_signals(symbols: list[str]):
    """Generate trading signals for given symbols."""
    try:
        return trading_service.generate_signals(symbols)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
