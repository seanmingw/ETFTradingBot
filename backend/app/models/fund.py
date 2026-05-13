"""Fund models supporting exchange (场内) and offline (场外) classification."""
from datetime import datetime
from typing import Optional, List, Literal
from pydantic import BaseModel, Field

FundType = Literal["exchange", "offline"]

class FundBase(BaseModel):
    symbol: str
    name: str
    fund_type: FundType
    category: Optional[str] = None
    region: Optional[str] = None
    expense_ratio: Optional[float] = None
    aum: Optional[int] = None

class ExchangeFund(FundBase):
    """Exchange traded fund (场内基金) - ETF, LOF, etc."""
    fund_type: FundType = "exchange"
    exchange: Optional[str] = None  # 'SSE', 'SZSE', 'NYSE'
    tracking_index: Optional[str] = None
    trading_currency: Optional[str] = "CNY"
    lot_size: Optional[int] = 100

class OfflineFund(FundBase):
    """Offline fund (场外基金) - Traditional mutual funds."""
    fund_type: FundType = "offline"
    fund_company: Optional[str] = None
    fund_manager: Optional[str] = None
    min_purchase: Optional[float] = 1.0
    subscription_fee: Optional[float] = 0.0
    redemption_fee: Optional[float] = 0.0

class FundInfo(FundBase):
    id: Optional[int] = None
    current_price: float
    daily_change: float
    daily_change_percent: float
    volume: int
    pe_ratio: Optional[float] = None
    fifty_two_week_high: float
    fifty_two_week_low: float
    ai_score: Optional[float] = None
    recommendation: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class FundScreenerRequest(BaseModel):
    fund_type: Optional[FundType] = None
    region: Optional[str] = None
    category: Optional[str] = None
    min_expense_ratio: Optional[float] = None
    max_expense_ratio: Optional[float] = None
    min_aum: Optional[int] = None
    risk_level: Optional[str] = None
    search_query: Optional[str] = None

class FundWithMetrics(FundInfo):
    momentum_score: Optional[float] = None
    trend_score: Optional[float] = None
    volatility_score: Optional[float] = None
    volume_score: Optional[float] = None
    risk_level: Optional[str] = None
    reason: Optional[str] = None
