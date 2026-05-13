"""Data models for ETF trading bot."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class ETFBase(BaseModel):
    symbol: str
    name: str
    category: Optional[str] = None
    region: Optional[str] = None
    expense_ratio: Optional[float] = None
    aum: Optional[int] = None

class ETFInfo(ETFBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ETFScreenerRequest(BaseModel):
    region: Optional[str] = None
    category: Optional[str] = None
    min_expense_ratio: Optional[float] = None
    max_expense_ratio: Optional[float] = None
    min_aum: Optional[int] = None
    risk_level: Optional[str] = None

class ETFWithMetrics(ETFInfo):
    current_price: float
    daily_change: float
    daily_change_percent: float
    volume: int
    pe_ratio: Optional[float] = None
    fifty_two_week_high: float
    fifty_two_week_low: float
    ai_score: Optional[float] = None
    recommendation: Optional[str] = None

class PriceData(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int

class PriceHistory(BaseModel):
    symbol: str
    prices: List[PriceData]
    indicators: Optional[dict] = None

class TechnicalIndicators(BaseModel):
    sma_5: Optional[float] = None
    sma_20: Optional[float] = None
    sma_50: Optional[float] = None
    sma_200: Optional[float] = None
    ema_12: Optional[float] = None
    ema_26: Optional[float] = None
    macd: Optional[float] = None
    macd_signal: Optional[float] = None
    macd_histogram: Optional[float] = None
    rsi: Optional[float] = None
    bollinger_upper: Optional[float] = None
    bollinger_middle: Optional[float] = None
    bollinger_lower: Optional[float] = None
    vwap: Optional[float] = None

class NewsItem(BaseModel):
    id: Optional[int] = None
    symbol: str
    title: str
    content: Optional[str] = None
    source: str
    url: Optional[str] = None
    sentiment: str
    sentiment_score: float
    published_at: datetime
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class NewsAnalysis(BaseModel):
    symbol: str
    news: List[NewsItem]
    overall_sentiment: str
    sentiment_score: float
    key_themes: List[str]
    impact_assessment: str
