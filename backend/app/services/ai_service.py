"""AI service for ETF analysis and recommendations."""
from typing import List, Dict, Optional
import logging
from datetime import datetime
from ..models.etf import ETFWithMetrics
from ..utils.indicators import calculate_sma, calculate_rsi, calculate_macd
from ..utils.market_data import MarketDataProvider

logger = logging.getLogger(__name__)

class AIService:
    """AI-powered ETF analysis and recommendation service."""

    def __init__(self):
        self.market_data = MarketDataProvider()

    def analyze_etf(self, symbol: str) -> Dict:
        """Perform comprehensive AI analysis on an ETF."""
        try:
            etf_info = self.market_data.get_etf_info(symbol)
            if not etf_info:
                return {'error': 'ETF not found'}

            price_data = self.market_data.get_price_history(symbol, period='6mo')
            if not price_data or not price_data['prices']:
                return {'error': 'Unable to fetch price history'}

            closes = [p['close'] for p in price_data['prices']]
            volumes = [p['volume'] for p in price_data['prices']]

            momentum_score = self._calculate_momentum(closes)
            trend_score = self._calculate_trend_strength(closes)
            volatility_score = self._calculate_volatility(closes)
            volume_score = self._analyze_volume(volumes)

            rsi = calculate_rsi(closes)
            rsi_value = rsi[-1] if rsi else 50

            overall_score = (
                momentum_score * 0.30 +
                trend_score * 0.25 +
                volatility_score * 0.20 +
                volume_score * 0.15 +
                (100 - abs(50 - rsi_value)) / 100 * 0.10
            )

            recommendation = self._generate_recommendation(
                overall_score, momentum_score, rsi_value
            )

            return {
                'symbol': symbol,
                'ai_score': round(overall_score, 2),
                'momentum_score': round(momentum_score, 2),
                'trend_score': round(trend_score, 2),
                'volatility_score': round(volatility_score, 2),
                'volume_score': round(volume_score, 2),
                'rsi': round(rsi_value, 2),
                'recommendation': recommendation['action'],
                'reason': recommendation['reason'],
                'risk_level': recommendation['risk'],
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error analyzing ETF {symbol}: {e}")
            return {'error': str(e)}

    def recommend_etfs(self, criteria: Dict) -> List[Dict]:
        """Recommend best ETFs based on criteria."""
        try:
            region = criteria.get('region')
            all_etfs = self.market_data.get_all_etfs_by_region(region)

            analyzed = []
            for etf_data in all_etfs[:20]:
                analysis = self.analyze_etf(etf_data['symbol'])
                if 'error' not in analysis:
                    analysis.update(etf_data)
                    analyzed.append(analysis)

            analyzed.sort(key=lambda x: x['ai_score'], reverse=True)

            return analyzed[:10]
        except Exception as e:
            logger.error(f"Error recommending ETFs: {e}")
            return []

    def _calculate_momentum(self, closes: List[float]) -> float:
        """Calculate momentum score based on price changes."""
        if len(closes) < 60:
            return 50

        returns_1m = (closes[-1] - closes[-20]) / closes[-20] * 100 if len(closes) >= 20 else 0
        returns_3m = (closes[-1] - closes[-60]) / closes[-60] * 100 if len(closes) >= 60 else 0
        returns_6m = (closes[-1] - closes[0]) / closes[0] * 100 if len(closes) >= 120 else 0

        momentum = (returns_1m * 0.5 + returns_3m * 0.3 + returns_6m * 0.2)

        return max(0, min(100, 50 + momentum * 5))

    def _calculate_trend_strength(self, closes: List[float]) -> float:
        """Calculate trend strength using moving averages."""
        if len(closes) < 200:
            return 50

        ma_20 = calculate_sma(closes, 20)
        ma_50 = calculate_sma(closes, 50)
        ma_200 = calculate_sma(closes, 200)

        if not ma_20 or not ma_50 or not ma_200:
            return 50

        current_price = closes[-1]
        ma20_current = ma_20[-1]
        ma50_current = ma_50[-1]
        ma200_current = ma_200[-1]

        trend_bullish = (
            current_price > ma20_current > ma50_current > ma200_current
        )

        trend_score = 0
        if trend_bullish:
            trend_score += 40
        elif current_price < ma20_current < ma50_current < ma200_current:
            trend_score += 10
        else:
            trend_score += 25

        price_strength = ((current_price - ma200_current) / ma200_current * 100) if ma200_current else 0
        trend_score += max(0, min(30, 15 + price_strength * 2))

        ma_slope = (ma_20[-1] - ma_20[-20]) / ma_20[-20] * 100 if len(ma_20) >= 20 else 0
        trend_score += max(0, min(30, 15 + ma_slope * 3))

        return max(0, min(100, trend_score))

    def _calculate_volatility(self, closes: List[float]) -> float:
        """Calculate volatility score (lower is better)."""
        if len(closes) < 20:
            return 50

        import numpy as np
        returns = np.diff(closes) / closes[:-1]
        volatility = np.std(returns) * np.sqrt(252) * 100

        ideal_volatility = 15
        if volatility < ideal_volatility:
            return 100 - volatility * 2
        else:
            return max(20, 100 - volatility)

    def _analyze_volume(self, volumes: List[int]) -> float:
        """Analyze volume trends."""
        if len(volumes) < 20:
            return 50

        avg_volume = sum(volumes[-20:]) / 20
        recent_volume = sum(volumes[-5:]) / 5

        volume_ratio = recent_volume / avg_volume if avg_volume > 0 else 1

        if volume_ratio > 1.5:
            return 80
        elif volume_ratio > 1.2:
            return 70
        elif volume_ratio > 0.8:
            return 60
        else:
            return 50

    def _generate_recommendation(self, overall_score: float, momentum: float, rsi: float) -> Dict:
        """Generate trading recommendation based on scores."""
        if overall_score >= 70 and rsi < 70:
            action = 'STRONG_BUY'
            reason = f'Strong momentum with AI score {overall_score:.1f}, RSI at {rsi:.1f}'
            risk = 'LOW'
        elif overall_score >= 60 and rsi < 65:
            action = 'BUY'
            reason = f'Positive signals with AI score {overall_score:.1f}'
            risk = 'MEDIUM'
        elif overall_score >= 50:
            action = 'HOLD'
            reason = f'Neutral outlook with AI score {overall_score:.1f}'
            risk = 'MEDIUM'
        elif overall_score >= 40 and rsi > 60:
            action = 'SELL'
            reason = f'Resistance levels with AI score {overall_score:.1f}, RSI at {rsi:.1f}'
            risk = 'HIGH'
        else:
            action = 'STRONG_SELL'
            reason = f'Negative momentum with AI score {overall_score:.1f}'
            risk = 'VERY_HIGH'

        return {
            'action': action,
            'reason': reason,
            'risk': risk
        }

    def predict_trend(self, symbol: str, days: int = 30) -> Dict:
        """Simple trend prediction using moving averages."""
        try:
            price_data = self.market_data.get_price_history(symbol, period='3mo')
            if not price_data or not price_data['prices']:
                return {'error': 'Unable to fetch price history'}

            closes = [p['close'] for p in price_data['prices']]

            ma_10 = calculate_sma(closes, 10)
            ma_30 = calculate_sma(closes, 30)

            if not ma_10 or not ma_30 or len(ma_10) < 2 or len(ma_30) < 2:
                return {'error': 'Insufficient data for prediction'}

            current_price = closes[-1]
            ma10_current = ma_10[-1]
            ma30_current = ma_30[-1]

            ma10_slope = (ma_10[-1] - ma_10[-5]) / ma_10[-5] * 100 if len(ma_10) >= 5 else 0
            ma30_slope = (ma_30[-1] - ma_30[-10]) / ma_30[-10] * 100 if len(ma_30) >= 10 else 0

            if ma10_current > ma30_current and ma10_slope > 0 and ma30_slope > 0:
                trend = 'BULLISH'
                confidence = min(95, 60 + ma10_slope + ma30_slope)
            elif ma10_current < ma30_current and ma10_slope < 0 and ma30_slope < 0:
                trend = 'BEARISH'
                confidence = min(95, 60 + abs(ma10_slope) + abs(ma30_slope))
            else:
                trend = 'NEUTRAL'
                confidence = 50

            predicted_change = (ma10_slope + ma30_slope) / 2 * days / 30
            predicted_price = current_price * (1 + predicted_change / 100)

            return {
                'symbol': symbol,
                'current_price': round(current_price, 2),
                'predicted_price_30d': round(predicted_price, 2),
                'predicted_change_percent': round(predicted_change, 2),
                'trend': trend,
                'confidence': round(confidence, 2),
                'ma10_slope': round(ma10_slope, 2),
                'ma30_slope': round(ma30_slope, 2),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error predicting trend for {symbol}: {e}")
            return {'error': str(e)}
