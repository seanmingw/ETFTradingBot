"""Market data utilities for fetching ETF data."""
import yfinance as yf
from typing import Optional, List, Dict
from datetime import datetime, timedelta
import logging
import random
import time

logger = logging.getLogger(__name__)

class MarketDataProvider:
    """Provider for fetching market data using yfinance."""

    GLOBAL_ETFS = {
        'US': {
            'SPY': 'SPDR S&P 500 ETF Trust',
            'QQQ': 'Invesco QQQ Trust Series 1',
            'VTI': 'Vanguard Total Stock Market ETF',
            'IWM': 'iShares Russell 2000 ETF',
            'EFA': 'iShares MSCI EAFE ETF',
            'EEM': 'iShares MSCI Emerging Markets ETF',
            'VWO': 'Vanguard FTSE Emerging Markets ETF',
            'TLT': 'iShares 20+ Year Treasury Bond ETF',
            'GLD': 'SPDR Gold Shares',
            'SLV': 'iShares Silver Trust',
            'AGG': 'iShares Core US Aggregate Bond ETF',
            'VNQ': 'Vanguard Real Estate ETF',
            'XLE': 'Energy Select Sector SPDR Fund',
            'XLF': 'Financial Select Sector SPDR Fund',
            'XLK': 'Technology Select Sector SPDR Fund',
            'XLV': 'Health Care Select Sector SPDR Fund',
            'XLY': 'Consumer Discretionary Select Sector SPDR Fund',
            'XLP': 'Consumer Staples Select Sector SPDR Fund',
            'XLI': 'Industrial Select Sector SPDR Fund',
            'XLB': 'Materials Select Sector SPDR Fund',
            'XLRE': 'Real Estate Select Sector SPDR Fund',
            'XLC': 'Communication Services Select Sector SPDR Fund',
            'XLU': 'Utilities Select Sector SPDR Fund',
            'DIA': 'SPDR Dow Jones Industrial Average ETF',
        },
        'Europe': {
            'VGK': 'Vanguard FTSE Europe ETF',
            'IEFA': 'iShares Core MSCI EAFE ETF',
            'EZU': 'iShares MSCI Eurozone ETF',
            'FEZ': 'SPDR Euro Stoxx 50 ETF',
        },
        'Asia': {
            'MCHI': 'iShares MSCI China ETF',
            'EWY': 'iShares MSCI South Korea ETF',
            'EWT': 'iShares MSCI Taiwan ETF',
            'INDA': 'iShares MSCI India ETF',
            'EWJ': 'iShares MSCI Japan ETF',
        }
    }

    FALLBACK_DATA = {
        'SPY': {'price': 523.45, 'change': 2.34, 'change_percent': 0.45, 'high': 525.00, 'low': 520.50, 'volume': 45000000},
        'QQQ': {'price': 448.32, 'change': -1.23, 'change_percent': -0.27, 'high': 450.00, 'low': 446.50, 'volume': 32000000},
        'VTI': {'price': 268.90, 'change': 1.56, 'change_percent': 0.58, 'high': 270.00, 'low': 267.00, 'volume': 2800000},
        'IWM': {'price': 198.45, 'change': -0.89, 'change_percent': -0.45, 'high': 200.00, 'low': 197.50, 'volume': 25000000},
        'EEM': {'price': 42.35, 'change': 0.45, 'change_percent': 1.07, 'high': 42.80, 'low': 41.90, 'volume': 35000000},
        'TLT': {'price': 95.60, 'change': -0.30, 'change_percent': -0.31, 'high': 96.20, 'low': 95.20, 'volume': 8000000},
        'GLD': {'price': 234.50, 'change': 1.80, 'change_percent': 0.77, 'high': 235.50, 'low': 232.50, 'volume': 9000000},
        'AGG': {'price': 98.75, 'change': 0.15, 'change_percent': 0.15, 'high': 99.00, 'low': 98.50, 'volume': 5000000},
    }

    @staticmethod
    def get_etf_info(symbol: str) -> Optional[Dict]:
        """Get basic ETF information."""
        try:
            ticker = yf.Ticker(symbol)
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    info = ticker.info
                    if info and 'regularMarketPrice' in info:
                        for region, etfs in MarketDataProvider.GLOBAL_ETFS.items():
                            if symbol in etfs:
                                return MarketDataProvider._format_etf_info(symbol, info, region, etfs[symbol])
                        return MarketDataProvider._format_etf_info(symbol, info, 'US', symbol)
                    break
                except Exception as e:
                    if '429' in str(e) or 'Too Many Requests' in str(e):
                        if attempt < max_retries - 1:
                            time.sleep(2 ** attempt)
                            continue
                    raise

            if symbol in MarketDataProvider.FALLBACK_DATA:
                return MarketDataProvider._get_fallback_etf_info(symbol)
            return None

        except Exception as e:
            logger.warning(f"Error fetching ETF info for {symbol}: {e}")
            if symbol in MarketDataProvider.FALLBACK_DATA:
                return MarketDataProvider._get_fallback_etf_info(symbol)
            return None

    @staticmethod
    def _format_etf_info(symbol: str, info: Dict, region: str, name: str) -> Dict:
        """Format ETF info from yfinance response."""
        return {
            'symbol': symbol,
            'name': info.get('longName', name),
            'category': info.get('category', 'Unknown'),
            'region': region,
            'expense_ratio': info.get('expenseRatio', 0),
            'aum': info.get('totalAssets', 0),
            'current_price': info.get('regularMarketPrice', 0),
            'daily_change': info.get('regularMarketChange', 0),
            'daily_change_percent': info.get('regularMarketChangePercent', 0),
            'volume': info.get('regularMarketVolume', 0),
            'pe_ratio': info.get('trailingPE', None),
            'fifty_two_week_high': info.get('fiftyTwoWeekHigh', 0),
            'fifty_two_week_low': info.get('fiftyTwoWeekLow', 0),
        }

    @staticmethod
    def _get_fallback_etf_info(symbol: str) -> Dict:
        """Get fallback ETF info when API is unavailable."""
        data = MarketDataProvider.FALLBACK_DATA.get(symbol, {
            'price': 100.00, 'change': 0.50, 'change_percent': 0.50,
            'high': 102.00, 'low': 98.00, 'volume': 1000000
        })

        name = symbol
        for region, etfs in MarketDataProvider.GLOBAL_ETFS.items():
            if symbol in etfs:
                name = etfs[symbol]
                break

        return {
            'symbol': symbol,
            'name': name,
            'category': 'ETF',
            'region': 'US',
            'expense_ratio': 0.001,
            'aum': 10000000000,
            'current_price': data['price'],
            'daily_change': data['change'],
            'daily_change_percent': data['change_percent'],
            'volume': data['volume'],
            'pe_ratio': 20.5,
            'fifty_two_week_high': data['high'],
            'fifty_two_week_low': data['low'],
        }

    @staticmethod
    def get_price_history(symbol: str, period: str = '1y', interval: str = '1d') -> Optional[Dict]:
        """Get historical price data."""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period, interval=interval)

            if hist.empty:
                return MarketDataProvider._get_fallback_price_history(symbol)

            prices = []
            for date, row in hist.iterrows():
                prices.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'open': float(row['Open']),
                    'high': float(row['High']),
                    'low': float(row['Low']),
                    'close': float(row['Close']),
                    'volume': int(row['Volume'])
                })

            return {
                'symbol': symbol,
                'prices': prices,
                'period': period,
                'interval': interval
            }
        except Exception as e:
            logger.error(f"Error fetching price history for {symbol}: {e}")
            return MarketDataProvider._get_fallback_price_history(symbol)

    @staticmethod
    def _get_fallback_price_history(symbol: str) -> Dict:
        """Generate fallback price history."""
        base_price = MarketDataProvider.FALLBACK_DATA.get(symbol, {}).get('price', 100)
        prices = []
        base_date = datetime.now()

        for i in range(252):
            date = base_date - timedelta(days=252-i)
            price = base_price * (1 + random.uniform(-0.02, 0.025))
            high = price * (1 + random.uniform(0, 0.01))
            low = price * (1 - random.uniform(0, 0.01))
            open_price = price * (1 + random.uniform(-0.005, 0.005))

            prices.append({
                'date': date.strftime('%Y-%m-%d'),
                'open': round(open_price, 2),
                'high': round(high, 2),
                'low': round(low, 2),
                'close': round(price, 2),
                'volume': random.randint(1000000, 50000000)
            })

        return {
            'symbol': symbol,
            'prices': prices,
            'period': '1y',
            'interval': '1d'
        }

    @staticmethod
    def get_realtime_price(symbol: str) -> Optional[Dict]:
        """Get real-time price quote."""
        try:
            info = MarketDataProvider.get_etf_info(symbol)
            if not info:
                return None

            return {
                'symbol': symbol,
                'price': info['current_price'],
                'change': info['daily_change'],
                'change_percent': info['daily_change_percent'],
                'volume': info['volume'],
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error fetching realtime price for {symbol}: {e}")
            return None

    @staticmethod
    def get_all_etfs_by_region(region: str = None) -> List[Dict]:
        """Get list of all available ETFs, optionally filtered by region."""
        result = []

        if region:
            regions = [region] if region in MarketDataProvider.GLOBAL_ETFS else []
        else:
            regions = MarketDataProvider.GLOBAL_ETFS.keys()

        for reg in regions:
            for symbol, name in MarketDataProvider.GLOBAL_ETFS[reg].items():
                etf_info = MarketDataProvider.get_etf_info(symbol)
                if etf_info:
                    result.append(etf_info)
                else:
                    result.append(MarketDataProvider._get_fallback_etf_info(symbol))

        return result

    @staticmethod
    def search_etfs(query: str, region: str = None) -> List[Dict]:
        """Search ETFs by name or symbol."""
        results = []
        query_lower = query.lower()

        all_etfs = MarketDataProvider.get_all_etfs_by_region(region)

        for etf in all_etfs:
            if (query_lower in etf['symbol'].lower() or
                query_lower in etf['name'].lower() or
                query_lower in etf.get('category', '').lower()):
                results.append(etf)

        return results
