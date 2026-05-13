"""News models."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class NewsArticle(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    source: str
    url: str
    published_at: datetime
    symbols: List[str] = []

class NewsResponse(BaseModel):
    articles: List[NewsArticle]
    total_results: int
    page: int = 1
    page_size: int = 20

class SentimentResult(BaseModel):
    label: str
    score: float
    confidence: float

class NewsSentiment(BaseModel):
    symbol: str
    articles: List[dict]
    overall_sentiment: str
    overall_score: float
    bullish_count: int
    bearish_count: int
    neutral_count: int
    average_score: float
