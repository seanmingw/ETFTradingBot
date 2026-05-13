"""ETF service for managing ETF data and operations."""
from typing import List, Optional, Dict
import logging
from ..utils.market_data import MarketDataProvider
from ..models.etf import ETFWithMetrics, ETFScreenerRequest, TechnicalIndicators
from ..utils.indicators import (
    calculate_sma, calculate_ema, calculate_rsi, calculate_macd,
    calculate_bollinger_bands, calculate_vwap
)

logger = logging.getLogger(__name__)

class ETFService:
    """Service for ETF data management and analysis."""

    def __init__(self):
        self.market_data = MarketDataProvider()

    def get_etf_by_symbol(self, symbol: str) -> Optional[ETFWithMetrics]:
        """Get detailed ETF information by symbol."""
        try:
            info = self.market_data.get_etf_info(symbol)
            if info:
                return ETFWithMetrics(**info)
            return None
        except Exception as e:
            logger.error(f"Error getting ETF {symbol}: {e}")
            return None

    def get_all_etfs(self, region: Optional[str] = None) -> List[ETFWithMetrics]:
        """Get all available ETFs, optionally filtered by region."""
        try:
            etfs = self.market_data.get_all_etfs_by_region(region)
            return [ETFWithMetrics(**etf) for etf in etfs if etf]
        except Exception as e:
            logger.error(f"Error getting all ETFs: {e}")
            return []

    def search_etfs(self, query: str, region: Optional[str] = None) -> List[ETFWithMetrics]:
        """Search ETFs by name or symbol."""
        try:
            results = self.market_data.search_etfs(query, region)
            return [ETFWithMetrics(**etf) for etf in results if etf]
        except Exception as e:
            logger.error(f"Error searching ETFs: {e}")
            return []

    def screen_etfs(self, criteria: ETFScreenerRequest) -> List[ETFWithMetrics]:
        """Screen ETFs based on given criteria."""
        try:
            etfs = self.get_all_etfs(region=criteria.region)

            filtered = []
            for etf in etfs:
                if criteria.category and etf.category != criteria.category:
                    continue
                if criteria.min_expense_ratio and (not etf.expense_ratio or etf.expense_ratio < criteria.min_expense_ratio):
                    continue
                if criteria.max_expense_ratio and (not etf.expense_ratio or etf.expense_ratio > criteria.max_expense_ratio):
                    continue
                if criteria.min_aum and (not etf.aum or etf.aum < criteria.min_aum):
                    continue
                filtered.append(etf)

            return filtered
        except Exception as e:
            logger.error(f"Error screening ETFs: {e}")
            return []

    def get_technical_indicators(self, symbol: str, period: str = '1y') -> Optional[TechnicalIndicators]:
        """Calculate technical indicators for an ETF."""
        try:
            price_data = self.market_data.get_price_history(symbol, period)
            if not price_data or not price_data['prices']:
                return None

            closes = [p['close'] for p in price_data['prices']]
            highs = [p['high'] for p in price_data['prices']]
            lows = [p['low'] for p in price_data['prices']]
            volumes = [p['volume'] for p in price_data['prices']]

            sma_5 = calculate_sma(closes, 5)
            sma_20 = calculate_sma(closes, 20)
            sma_50 = calculate_sma(closes, 50)
            sma_200 = calculate_sma(closes, 200)
            ema_12 = calculate_ema(closes, 12)
            ema_26 = calculate_ema(closes, 26)

            macd_line, signal_line, histogram = calculate_macd(closes)
            rsi = calculate_rsi(closes)
            upper_bb, middle_bb, lower_bb = calculate_bollinger_bands(closes)
            vwap = calculate_vwap(highs, lows, closes, volumes)

            latest_close = closes[-1] if closes else 0

            return TechnicalIndicators(
                sma_5=sma_5[-1] if sma_5 else None,
                sma_20=sma_20[-1] if sma_20 else None,
                sma_50=sma_50[-1] if sma_50 else None,
                sma_200=sma_200[-1] if sma_200 else None,
                ema_12=ema_12[-1] if ema_12 else None,
                ema_26=ema_26[-1] if ema_26 else None,
                macd=macd_line[-1] if macd_line else None,
                macd_signal=signal_line[-1] if signal_line else None,
                macd_histogram=histogram[-1] if histogram else None,
                rsi=rsi[-1] if rsi else None,
                bollinger_upper=upper_bb[-1] if upper_bb else None,
                bollinger_middle=middle_bb[-1] if middle_bb else None,
                bollinger_lower=lower_bb[-1] if lower_bb else None,
                vwap=vwap[-1] if vwap else None
            )
        except Exception as e:
            logger.error(f"Error calculating indicators for {symbol}: {e}")
            return None

    def get_etf_comparison(self, symbols: List[str]) -> List[Dict]:
        """Compare multiple ETFs."""
        try:
            comparisons = []
            for symbol in symbols:
                etf = self.get_etf_by_symbol(symbol)
                if etf:
                    comparisons.append({
                        'symbol': symbol,
                        'name': etf.name,
                        'price': etf.current_price,
                        'change_percent': etf.daily_change_percent,
                        'volume': etf.volume,
                        'pe_ratio': etf.pe_ratio,
                        'week_52_high': etf.fifty_two_week_high,
                        'week_52_low': etf.fifty_two_week_low,
                        'position_vs_high': ((etf.current_price - etf.fifty_two_week_low) /
                                            (etf.fifty_two_week_high - etf.fifty_two_week_low) * 100)
                                            if etf.fifty_two_week_high != etf.fifty_two_week_low else 50
                    })
            return comparisons
        except Exception as e:
            logger.error(f"Error comparing ETFs: {e}")
            return []
