"""Trading models."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class TradeRequest(BaseModel):
    symbol: str
    action: str = Field(..., pattern="^(buy|sell)$")
    quantity: int = Field(..., gt=0)
    order_type: str = Field(default="market", pattern="^(market|limit|stop_loss|take_profit)$")
    limit_price: Optional[float] = None
    strategy: Optional[str] = "manual"

class TradeResponse(BaseModel):
    id: int
    symbol: str
    action: str
    quantity: int
    price: float
    commission: float
    total_amount: float
    strategy: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class Position(BaseModel):
    id: Optional[int] = None
    symbol: str
    quantity: int
    avg_cost: float
    current_price: float
    market_value: float
    unrealized_pnl: float
    unrealized_pnl_percent: float
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PortfolioSummary(BaseModel):
    total_value: float
    total_cost: float
    total_pnl: float
    total_pnl_percent: float
    day_pnl: float
    day_pnl_percent: float
    positions: list[Position]
    cash: float
    buying_power: float

class StrategyConfig(BaseModel):
    name: str
    enabled: bool = True
    max_position_size: float = 0.2
    stop_loss_percent: float = 0.03
    take_profit_percent: float = 0.08
    max_daily_trades: int = 10

class TradingSignal(BaseModel):
    symbol: str
    action: str
    confidence: float
    strategy: str
    reason: str
    entry_price: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    timestamp: datetime
