"""Technical analysis service for advanced market analysis."""
from typing import Dict, Optional, List
from datetime import datetime
import logging
from ..utils.market_data import MarketDataProvider
from ..utils.indicators import (
    calculate_sma, calculate_ema, calculate_rsi, calculate_macd,
    calculate_bollinger_bands, calculate_vwap, calculate_atr, calculate_stochastic
)

logger = logging.getLogger(__name__)

class AnalysisService:
    """Service for advanced technical analysis."""

    def __init__(self):
        self.market_data = MarketDataProvider()

    def comprehensive_analysis(self, symbol: str, period: str = '1y') -> Dict:
        """Perform comprehensive technical analysis."""
        try:
            price_data = self.market_data.get_price_history(symbol, period)
            if not price_data or not price_data['prices']:
                return {'error': 'Unable to fetch price data'}

            prices = price_data['prices']
            closes = [p['close'] for p in prices]
            highs = [p['high'] for p in prices]
            lows = [p['low'] for p in prices]
            volumes = [p['volume'] for p in prices]

            analysis = {
                'symbol': symbol,
                'timestamp': datetime.now().isoformat(),
                'price_action': self._analyze_price_action(prices),
                'trend_analysis': self._analyze_trends(closes),
                'momentum_indicators': self._analyze_momentum(closes, highs, lows),
                'volume_analysis': self._analyze_volume(volumes, closes),
                'support_resistance': self._find_support_resistance(closes, highs, lows),
                'pattern_recognition': self._recognize_patterns(closes, highs, lows),
                'signals': self._generate_signals(closes, highs, lows, volumes)
            }

            return analysis
        except Exception as e:
            logger.error(f"Error in comprehensive analysis for {symbol}: {e}")
            return {'error': str(e)}

    def _analyze_price_action(self, prices: List[Dict]) -> Dict:
        """Analyze price action."""
        if len(prices) < 2:
            return {}

        current = prices[-1]
        prev = prices[-2]

        change = current['close'] - prev['close']
        change_percent = (change / prev['close'] * 100) if prev['close'] > 0 else 0

        high_low_52w = max(p['high'] for p in prices[-252:]) if len(prices) >= 252 else max(p['high'] for p in prices)
        low_low_52w = min(p['low'] for p in prices[-252:]) if len(prices) >= 252 else min(p['low'] for p in prices)

        closes = [p['close'] for p in prices]
        avg_gain = sum(max(closes[i] - closes[i-1], 0) for i in range(1, len(closes))) / len(closes)
        avg_loss = sum(max(closes[i-1] - closes[i], 0) for i in range(1, len(closes))) / len(closes)

        return {
            'current_price': current['close'],
            'change': round(change, 2),
            'change_percent': round(change_percent, 2),
            '52_week_high': round(high_low_52w, 2),
            '52_week_low': round(low_low_52w, 2),
            'position_vs_52w_high': round((current['close'] - low_low_52w) / (high_low_52w - low_low_52w) * 100, 2) if high_low_52w != low_low_52w else 50,
            'average_gain': round(avg_gain, 4),
            'average_loss': round(avg_loss, 4)
        }

    def _analyze_trends(self, closes: List[float]) -> Dict:
        """Analyze trend using multiple timeframes."""
        if len(closes) < 200:
            return {}

        sma_20 = calculate_sma(closes, 20)
        sma_50 = calculate_sma(closes, 50)
        sma_200 = calculate_sma(closes, 200)

        current_price = closes[-1]

        trend = 'NEUTRAL'
        trend_strength = 50

        if len(sma_20) > 0 and len(sma_50) > 0 and len(sma_200) > 0:
            if current_price > sma_20[-1] > sma_50[-1] > sma_200[-1]:
                trend = 'STRONG_UPTREND'
                trend_strength = 85
            elif current_price > sma_20[-1] > sma_50[-1]:
                trend = 'UPTREND'
                trend_strength = 70
            elif current_price < sma_20[-1] < sma_50[-1] < sma_200[-1]:
                trend = 'STRONG_DOWNTREND'
                trend_strength = 85
            elif current_price < sma_20[-1] < sma_50[-1]:
                trend = 'DOWNTREND'
                trend_strength = 70

            price_vs_ma200 = ((current_price - sma_200[-1]) / sma_200[-1] * 100) if sma_200[-1] > 0 else 0

            return {
                'trend': trend,
                'trend_strength': trend_strength,
                'sma_20': round(sma_20[-1], 2),
                'sma_50': round(sma_50[-1], 2),
                'sma_200': round(sma_200[-1], 2) if len(sma_200) > 0 else None,
                'price_vs_ma200_percent': round(price_vs_ma200, 2),
                'trend_direction': 'BULLISH' if sma_20[-1] > sma_50[-1] else 'BEARISH'
            }

        return {}

    def _analyze_momentum(self, closes: List[float], highs: List[float], lows: List[float]) -> Dict:
        """Analyze momentum indicators."""
        rsi = calculate_rsi(closes, 14)
        macd_line, signal_line, histogram = calculate_macd(closes)
        k_values, d_values = calculate_stochastic(highs, lows, closes, 14)

        rsi_value = rsi[-1] if rsi else 50
        macd_value = macd_line[-1] if macd_line else 0
        signal_value = signal_line[-1] if signal_line else 0
        histogram_value = histogram[-1] if histogram else 0
        k_value = k_values[-1] if k_values else 50
        d_value = d_values[-1] if d_values else 50

        rsi_signal = 'OVERBOUGHT' if rsi_value > 70 else 'OVERSOLD' if rsi_value < 30 else 'NEUTRAL'
        stoch_signal = 'OVERBOUGHT' if k_value > 80 else 'OVERSOLD' if k_value < 20 else 'NEUTRAL'
        macd_signal = 'BULLISH' if histogram_value > 0 else 'BEARISH'

        return {
            'rsi': {
                'value': round(rsi_value, 2),
                'signal': rsi_signal
            },
            'macd': {
                'value': round(macd_value, 4),
                'signal': round(signal_value, 4),
                'histogram': round(histogram_value, 4),
                'interpretation': macd_signal
            },
            'stochastic': {
                'k': round(k_value, 2),
                'd': round(d_value, 2),
                'signal': stoch_signal
            }
        }

    def _analyze_volume(self, volumes: List[int], closes: List[float]) -> Dict:
        """Analyze volume patterns."""
        if len(volumes) < 20:
            return {}

        avg_volume_20 = sum(volumes[-20:]) / 20
        avg_volume_5 = sum(volumes[-5:]) / 5
        current_volume = volumes[-1]

        volume_ratio = avg_volume_5 / avg_volume_20 if avg_volume_20 > 0 else 1

        price_change = (closes[-1] - closes[-2]) / closes[-2] * 100 if len(closes) >= 2 else 0

        if volume_ratio > 1.5 and price_change > 0:
            volume_signal = 'STRONG_BUY'
        elif volume_ratio > 1.5 and price_change < 0:
            volume_signal = 'STRONG_SELL'
        elif volume_ratio < 0.7:
            volume_signal = 'LOW_VOLUME'
        else:
            volume_signal = 'NORMAL'

        return {
            'current_volume': current_volume,
            'avg_volume_20d': round(avg_volume_20, 0),
            'volume_ratio': round(volume_ratio, 2),
            'price_change_with_volume': round(price_change, 2),
            'signal': volume_signal
        }

    def _find_support_resistance(self, closes: List[float], highs: List[float], lows: List[float]) -> Dict:
        """Find support and resistance levels."""
        if len(closes) < 50:
            return {}

        import numpy as np

        price_percentiles = np.percentile(closes[-50:], [20, 40, 60, 80])

        return {
            'strong_resistance': round(max(highs[-50:]), 2),
            'resistance_1': round(price_percentiles[3], 2),
            'pivot': round(price_percentiles[2], 2),
            'support_1': round(price_percentiles[1], 2),
            'strong_support': round(min(lows[-50:]), 2)
        }

    def _recognize_patterns(self, closes: List[float], highs: List[float], lows: List[float]) -> List[str]:
        """Recognize chart patterns."""
        patterns = []

        if len(closes) < 50:
            return patterns

        recent_closes = closes[-20:]
        recent_highs = highs[-20:]
        recent_lows = lows[-20:]

        if all(closes[i] > closes[i-1] for i in range(1, len(closes[-10:]))):
            patterns.append('ASCENDING_TRIANGLE')

        if all(closes[i] < closes[i-1] for i in range(1, len(closes[-10:]))):
            patterns.append('DESCENDING_TRIANGLE')

        if recent_lows[-1] > min(recent_lows[-10:]) and recent_highs[-1] > max(recent_highs[-10:-1]):
            patterns.append('HIGHER_LOW_HIGHER_HIGH')

        if recent_highs[-1] < max(recent_highs[-10:]) and recent_lows[-1] < min(recent_lows[-10:-1]):
            patterns.append('LOWER_HIGH_LOWER_LOW')

        return patterns

    def _generate_signals(self, closes: List[float], highs: List[float], lows: List[float], volumes: List[int]) -> Dict:
        """Generate trading signals based on all indicators."""
        signals = []

        rsi = calculate_rsi(closes, 14)
        rsi_value = rsi[-1] if rsi else 50

        if rsi_value < 30:
            signals.append({
                'type': 'RSI_OVERSOLD',
                'action': 'BUY',
                'confidence': round(100 - rsi_value, 2),
                'reason': 'RSI indicates oversold condition'
            })
        elif rsi_value > 70:
            signals.append({
                'type': 'RSI_OVERBOUGHT',
                'action': 'SELL',
                'confidence': round(rsi_value, 2),
                'reason': 'RSI indicates overbought condition'
            })

        macd_line, signal_line, histogram = calculate_macd(closes)
        if len(histogram) >= 2 and histogram[-1] > 0 and histogram[-2] < 0:
            signals.append({
                'type': 'MACD_CROSS_UP',
                'action': 'BUY',
                'confidence': 80,
                'reason': 'MACD bullish crossover'
            })
        elif len(histogram) >= 2 and histogram[-1] < 0 and histogram[-2] > 0:
            signals.append({
                'type': 'MACD_CROSS_DOWN',
                'action': 'SELL',
                'confidence': 80,
                'reason': 'MACD bearish crossover'
            })

        upper_bb, middle_bb, lower_bb = calculate_bollinger_bands(closes, 20, 2)
        if len(lower_bb) > 0 and closes[-1] <= lower_bb[-1]:
            signals.append({
                'type': 'BOLLINGER_TOUCH_LOWER',
                'action': 'BUY',
                'confidence': 75,
                'reason': 'Price at lower Bollinger Band'
            })
        elif len(upper_bb) > 0 and closes[-1] >= upper_bb[-1]:
            signals.append({
                'type': 'BOLLINGER_TOUCH_UPPER',
                'action': 'SELL',
                'confidence': 75,
                'reason': 'Price at upper Bollinger Band'
            })

        buy_signals = [s for s in signals if s['action'] == 'BUY']
        sell_signals = [s for s in signals if s['action'] == 'SELL']

        overall_signal = 'NEUTRAL'
        if len(buy_signals) > len(sell_signals):
            overall_signal = 'BUY'
        elif len(sell_signals) > len(buy_signals):
            overall_signal = 'SELL'

        return {
            'overall_signal': overall_signal,
            'individual_signals': signals,
            'buy_signals_count': len(buy_signals),
            'sell_signals_count': len(sell_signals)
        }
