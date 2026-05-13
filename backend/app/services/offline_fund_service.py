"""Offline fund service (场外基金)."""
from typing import List, Optional, Dict
import logging
import random

logger = logging.getLogger(__name__)

class OfflineFundService:
    """Service for offline traded funds (场外基金)."""

    OFFLINE_FUNDS = {
        'Equity': {
            '000001': '华夏上证50ETF联接A',
            '000311': '景顺长城沪深300ETF联接',
            '110022': '易方达上证50指数A',
            '160706': '嘉实沪深300ETF联接A',
            '161725': '招商中证白酒指数',
            '001632': '天弘中证500ETF联接A',
            '003095': '中欧医疗健康混合A',
            '000961': '天弘永定价值成长混合',
            '163402': '兴全趋势投资混合',
            '519069': '汇添富价值精选混合',
        },
        'Bond': {
            '001236': '博时黄金ETF联接A',
            '002400': '广发中债7-10年国开债指数A',
            '217022': '招商招财金融债定期开放债券',
            '003547': '鹏华丰禄债券',
            '000286': '华夏债券A/B',
        },
        'Index': {
            '050002': '博时沪深300指数A',
            '270010': '广发沪深300ETF联接',
            '160119': '易方达中证500ETF联接A',
            '100032': '富国中证红利指数增强',
        },
        'International': {
            '000071': '华夏恒生ETF联接A',
            '270042': '广发纳斯达克100指数',
            '040046': '华安纳斯达克100指数',
            '001668': '汇添富全球互联混合',
        }
    }

    FUND_COMPANIES = {
        '000001': '华夏基金',
        '000311': '景顺长城基金',
        '110022': '易方达基金',
        '160706': '嘉实基金',
        '161725': '招商基金',
        '001632': '天弘基金',
        '003095': '中欧基金',
        '000961': '天弘基金',
        '163402': '兴全基金',
        '519069': '汇添富基金',
    }

    def get_offline_funds_by_category(self, category: str = None) -> List[Dict]:
        """Get offline funds by category."""
        try:
            result = []
            categories = [category] if category else self.OFFLINE_FUNDS.keys()

            for cat in categories:
                if cat not in self.OFFLINE_FUNDS:
                    continue

                for symbol, name in self.OFFLINE_FUNDS[cat].items():
                    fund_info = self._get_fallback_fund_info(symbol, name, cat)
                    result.append(fund_info)

            return result
        except Exception as e:
            logger.error(f"Error getting offline funds: {e}")
            return []

    def get_all_offline_funds(self) -> List[Dict]:
        """Get all offline funds."""
        return self.get_offline_funds_by_category()

    def get_fund_by_symbol(self, symbol: str) -> Optional[Dict]:
        """Get offline fund details by symbol."""
        try:
            for category, funds in self.OFFLINE_FUNDS.items():
                if symbol in funds:
                    return self._get_fallback_fund_info(symbol, funds[symbol], category)

            if symbol in self.FUND_COMPANIES:
                category = 'Equity'
                name = symbol
                return self._get_fallback_fund_info(symbol, name, category)

            return None
        except Exception as e:
            logger.error(f"Error getting fund {symbol}: {e}")
            return None

    def _get_fallback_fund_info(self, symbol: str, name: str, category: str) -> Dict:
        """Get fallback fund info."""
        base_prices = {
            '000001': 1.85, '000311': 2.45, '110022': 3.20, '160706': 1.65,
            '161725': 1.92, '001632': 1.35, '003095': 2.80, '000961': 2.15,
            '163402': 1.48, '519069': 3.65, '050002': 2.25, '270010': 1.95,
        }

        base_price = base_prices.get(symbol, 1.5)
        change = random.uniform(-0.015, 0.015)

        category_map = {
            'Equity': '股票型',
            'Bond': '债券型',
            'Index': '指数型',
            'International': 'QDII'
        }

        return {
            'symbol': symbol,
            'name': name,
            'fund_type': 'offline',
            'category': category_map.get(category, '混合型'),
            'category_en': category,
            'region': 'China',
            'fund_company': self.FUND_COMPANIES.get(symbol, '基金公司'),
            'fund_manager': self._generate_manager_name(),
            'expense_ratio': random.uniform(0.3, 1.5) / 100,
            'aum': random.randint(5000000000, 50000000000),
            'current_price': round(base_price * (1 + change), 3),
            'daily_change': round(base_price * change, 4),
            'daily_change_percent': round(change * 100, 2),
            'volume': random.randint(100000, 5000000),
            'pe_ratio': round(random.uniform(10, 30), 2),
            'fifty_two_week_high': round(base_price * 1.3, 3),
            'fifty_two_week_low': round(base_price * 0.7, 3),
            'min_purchase': 10.0 if 'ETF联接' in name else 100.0,
            'subscription_fee': round(random.uniform(0, 0.15), 3),
            'redemption_fee': round(random.uniform(0, 0.5), 3),
        }

    def _generate_manager_name(self) -> str:
        """Generate a random fund manager name."""
        surnames = ['张', '王', '李', '刘', '陈', '杨', '赵', '黄', '周', '吴']
        names = ['明', '强', '伟', '芳', '娜', '敏', '静', '丽', '涛', '华']
        return f"{random.choice(surnames)}{random.choice(names)}"
