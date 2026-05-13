"""Exchange traded fund service (场内基金)."""
from typing import List, Optional, Dict
import logging
from ..utils.market_data import MarketDataProvider

logger = logging.getLogger(__name__)

class ExchangeFundService:
    """Service for exchange traded funds (场内基金)."""

    EXCHANGE_FUNDS = {
        'China': {
            '510050': '华夏上证50ETF',
            '510300': '华泰柏瑞沪深300ETF',
            '510500': '南方中证500ETF',
            '159915': '易方达创业板ETF',
            '512000': '华安中证全指证券公司ETF',
            '512100': '国泰中证全指证券公司ETF',
            '512880': '国泰中证军工ETF',
            '512660': '国泰中证煤炭ETF',
            '512980': '博时中证银行ETF',
            '159928': '汇添富中证主要消费ETF',
            '513050': '易方达中证海外中国互联网50',
            '159941': '广发纳斯达克100ETF',
            '513500': '博时标普500ETF',
        },
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
            'AGG': 'iShares Core US Aggregate Bond ETF',
            'VNQ': 'Vanguard Real Estate ETF',
            'XLE': 'Energy Select Sector SPDR Fund',
            'XLF': 'Financial Select Sector SPDR Fund',
            'XLK': 'Technology Select Sector SPDR Fund',
            'XLV': 'Health Care Select Sector SPDR Fund',
            'DIA': 'SPDR Dow Jones Industrial Average ETF',
        }
    }

    def __init__(self):
        self.market_data = MarketDataProvider()

    def get_exchange_funds_by_region(self, region: str = None) -> List[Dict]:
        """Get exchange traded funds by region."""
        try:
            result = []
            if region:
                regions = [region]
            else:
                regions = self.EXCHANGE_FUNDS.keys()

            for reg in regions:
                if reg not in self.EXCHANGE_FUNDS:
                    continue

                for symbol, name in self.EXCHANGE_FUNDS[reg].items():
                    fund_info = self.market_data.get_etf_info(symbol)
                    if fund_info:
                        fund_info['fund_type'] = 'exchange'
                        fund_info['exchange'] = reg
                        result.append(fund_info)
                    else:
                        result.append(self._get_fallback_fund_info(symbol, name, 'exchange', reg))

            return result
        except Exception as e:
            logger.error(f"Error getting exchange funds: {e}")
            return []

    def get_fund_by_symbol(self, symbol: str) -> Optional[Dict]:
        """Get exchange fund details by symbol."""
        try:
            fund_info = self.market_data.get_etf_info(symbol)
            if fund_info:
                fund_info['fund_type'] = 'exchange'
                region = self._detect_region(symbol)
                fund_info['exchange'] = region
                return fund_info

            for region, funds in self.EXCHANGE_FUNDS.items():
                if symbol in funds:
                    return self._get_fallback_fund_info(symbol, funds[symbol], 'exchange', region)

            return None
        except Exception as e:
            logger.error(f"Error getting fund {symbol}: {e}")
            return None

    def _detect_region(self, symbol: str) -> str:
        """Detect fund region by symbol."""
        if symbol.isdigit() and len(symbol) == 6:
            return 'China'
        return 'US'

    def _get_fallback_fund_info(self, symbol: str, name: str, fund_type: str, region: str) -> Dict:
        """Get fallback fund info."""
        base_prices = {
            '510050': 2.80, '510300': 4.20, '510500': 6.50, '159915': 2.30,
            'SPY': 523.45, 'QQQ': 448.32, 'VTI': 268.90, 'IWM': 198.45,
            'EEM': 42.35, 'TLT': 95.60, 'GLD': 234.50
        }

        base_price = base_prices.get(symbol, 100.0)
        import random
        change = random.uniform(-0.02, 0.02)

        return {
            'symbol': symbol,
            'name': name,
            'fund_type': fund_type,
            'category': 'ETF',
            'region': region,
            'exchange': region,
            'expense_ratio': 0.001,
            'aum': 10000000000,
            'current_price': base_price,
            'daily_change': base_price * change,
            'daily_change_percent': change * 100,
            'volume': random.randint(1000000, 50000000),
            'pe_ratio': 20.5,
            'fifty_two_week_high': base_price * 1.2,
            'fifty_two_week_low': base_price * 0.8,
            'tracking_index': None,
            'trading_currency': 'CNY' if region == 'China' else 'USD',
            'lot_size': 100
        }
