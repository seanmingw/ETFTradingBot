"""News API routes."""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from ..services.news_service import NewsService
from datetime import datetime

router = APIRouter(prefix="/api/news", tags=["News"])

news_service = NewsService()

@router.get("/{symbol}")
async def get_news(symbol: str, limit: int = Query(default=20, ge=1, le=50)):
    """Get news articles for a specific ETF symbol."""
    try:
        news = news_service.get_news_for_symbol(symbol.upper(), limit)
        return {
            'symbol': symbol.upper(),
            'news': news,
            'total': len(news),
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sentiment/{symbol}")
async def get_news_sentiment(symbol: str):
    """Get sentiment analysis for news about an ETF."""
    try:
        news = news_service.get_news_for_symbol(symbol.upper(), 20)
        sentiment = news_service.analyze_sentiment(news)
        return {
            'symbol': symbol.upper(),
            'sentiment': sentiment,
            'news_count': len(news),
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/related/{symbol}")
async def get_related_news(symbol: str, related: Optional[str] = Query(default=None)):
    """Get news for symbol and related ETFs."""
    try:
        related_symbols = [r.strip().upper() for r in related.split(',')] if related else []
        news_data = news_service.get_related_news(symbol.upper(), related_symbols)
        return news_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/market/overview")
async def get_market_overview():
    """Get overall market news and sentiment."""
    try:
        return news_service.get_market_overview()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
