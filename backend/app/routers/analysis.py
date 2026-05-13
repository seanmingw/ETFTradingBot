"""Analysis API routes."""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, Dict
from ..services.ai_service import AIService
from ..services.analysis_service import AnalysisService
from ..services.etf_service import ETFService
from ..utils.market_data import MarketDataProvider

router = APIRouter(prefix="/api/analysis", tags=["Analysis"])

ai_service = AIService()
analysis_service = AnalysisService()
etf_service = ETFService()
market_data = MarketDataProvider()

@router.post("/predict")
async def predict_etf_trend(symbol: str, days: int = Query(default=30, ge=7, le=90)):
    """Get AI trend prediction for an ETF."""
    try:
        prediction = ai_service.predict_trend(symbol.upper(), days)
        if 'error' in prediction:
            raise HTTPException(status_code=404, detail=prediction['error'])
        return prediction
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recommend")
async def recommend_etfs(region: Optional[str] = None, limit: int = Query(default=10, ge=1, le=20)):
    """Get AI-powered ETF recommendations."""
    try:
        criteria = {'region': region}
        recommendations = ai_service.recommend_etfs(criteria)
        return {
            'recommendations': recommendations[:limit],
            'total': len(recommendations),
            'timestamp': analysis_service._get_timestamp()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{symbol}")
async def get_comprehensive_analysis(symbol: str, period: str = Query(default="1y")):
    """Get comprehensive technical analysis for an ETF."""
    try:
        analysis = analysis_service.comprehensive_analysis(symbol.upper(), period)
        if 'error' in analysis:
            raise HTTPException(status_code=404, detail=analysis['error'])
        return analysis
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/technicals/{symbol}")
async def get_technicals(symbol: str, period: str = Query(default="1y")):
    """Get technical indicators for an ETF."""
    try:
        analysis = analysis_service.comprehensive_analysis(symbol.upper(), period)
        if 'error' in analysis:
            raise HTTPException(status_code=404, detail=analysis['error'])
        return {
            'symbol': symbol.upper(),
            'trend_analysis': analysis.get('trend_analysis', {}),
            'momentum_indicators': analysis.get('momentum_indicators', {}),
            'volume_analysis': analysis.get('volume_analysis', {}),
            'support_resistance': analysis.get('support_resistance', {}),
            'patterns': analysis.get('pattern_recognition', []),
            'signals': analysis.get('signals', {})
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/signals/{symbol}")
async def get_signals(symbol: str):
    """Get trading signals for an ETF."""
    try:
        analysis = analysis_service.comprehensive_analysis(symbol.upper())
        if 'error' in analysis:
            raise HTTPException(status_code=404, detail=analysis['error'])
        return {
            'symbol': symbol.upper(),
            'overall_signal': analysis['signals']['overall_signal'],
            'signals': analysis['signals']['individual_signals'],
            'buy_count': analysis['signals']['buy_signals_count'],
            'sell_count': analysis['signals']['sell_signals_count']
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def _get_timestamp(self):
    """Helper to get current timestamp."""
    from datetime import datetime
    return datetime.now().isoformat()
